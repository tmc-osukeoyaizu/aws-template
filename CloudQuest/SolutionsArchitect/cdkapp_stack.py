from aws_cdk import (
Duration,
Stack,
SecretValue,
aws_ec2 as ec2,
aws_rds as rds,
aws_iam as iam,
aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct

class CdkappStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here


        # create a vpc with IpAddresses 10.10.0.0/16, a NAT gateway, a public subnet, PRIVATE_WITH_EGRESS subnet and a RDS subne
        vpc = ec2.Vpc(
            self, "CdkappVpc",
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private_with_egress",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # create a security group for the load balancer
        alb_security_group = ec2.SecurityGroup(
            self, "CdkappALBSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )

        # create a security group for the RDS instance
        rds_security_group = ec2.SecurityGroup(
            self, "CdkappRDSSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )

        # create a security group for the EC2 instance
        ec2_security_group = ec2.SecurityGroup(
            self, "CdkappEC2SecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )


        # add ingress rules for the load balancer security group to allow all traffic on port 80
        alb_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow all traffic on port 80"
        )

        # add ingress rule for the EC2 instance security group to allow 8443 traffic from the load balancer
        ec2_security_group.add_ingress_rule(
            peer=alb_security_group,
            connection=ec2.Port.tcp(8443),
            description="Allow traffic from load balancer"
        )

        # add ingress rule to RDS security group to allow 3306 traffic from EC2 security group
        rds_security_group.add_ingress_rule(
            peer=ec2_security_group,
            connection=ec2.Port.tcp(3306),
            description="Allow traffic from EC2 security group"
        )

        # add ingress rule for the RDS security group to allow 22 from the EC2 instance
        rds_security_group.add_ingress_rule(
            peer=ec2_security_group,
            connection=ec2.Port.tcp(22),
            description="Allow traffic from EC2 security group"
        )


        # create an rds aurora mysql cluster
        cluster = rds.DatabaseCluster(self, "MyDatabase",
            engine = rds.DatabaseClusterEngine.aurora_mysql(version = rds.AuroraMysqlEngineVersion.VER_3_04_0),
            # credentials using testuser and password1234!
            credentials = rds.Credentials.from_password("testuser", SecretValue.unsafe_plain_text("password1234!")),
            # add default database name Population
            default_database_name = "Population",
            instance_props={
                "vpc": vpc,
                "security_groups": [rds_security_group],
                "vpc_subnets": ec2.SubnetSelection(subnet_type = ec2.SubnetType.PRIVATE_ISOLATED)
            },
            instances = 1
            )

        # define an Amazon Linux 2023 image
        ami = ec2.MachineImage.latest_amazon_linux2023()
        
        # read userdata file from cdkapp directory using readlines
        with open("cdkapp/userdata.sh", "r") as f:
            userdata = f.readlines()

        # Add each line from the script to ec2 UserData
        user_data = ec2.UserData.for_linux()
        for line in userdata:
            user_data.add_commands(line.strip())
        
        
        # create a t3.small ec2 instance for the web server in a private egress subnet and vpc.availability_zones[0]
        ec2_instance = ec2.Instance(self, "MyInstance",
            instance_type = ec2.InstanceType("t3.small"),
            machine_image = ami,
            vpc = vpc,
            vpc_subnets = ec2.SubnetSelection(subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS),
            availability_zone = vpc.availability_zones[0],
            user_data = user_data,
            security_group = ec2_security_group,
            # add an existing role with name ec2_instance_role
            role = iam.Role.from_role_name(self, "ec2_instance_role", "ec2_instance_role")
        )

        # add depends
        ec2_instance.node.add_dependency(cluster)


        ec2_instance2 = ec2.Instance(self, "MyInstance2",
            instance_type = ec2.InstanceType("t3.small"),
            machine_image = ami,
            vpc = vpc,
            vpc_subnets = ec2.SubnetSelection(subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS),
            availability_zone = vpc.availability_zones[1],
            user_data = user_data,
            security_group = ec2_security_group,
            # add an existing role with name ec2_instance_role
            role = iam.Role.from_role_name(self, "ec2_instance_role2", "ec2_instance_role")
        )

        # add depends
        ec2_instance2.node.add_dependency(cluster)

        # create a load balancer in the public subnet
        alb = elbv2.ApplicationLoadBalancer(
            self, "CdkappALB",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_security_group
        )

        # add a listener on port 80 to the load balancer with open=True
        listener = alb.add_listener("CdkappListener", port=80, open=True)

        # add targets to the load balancer using port 80 with unhealthy healthcheck threshold count 5
        listener.add_targets("CdkappTarget", port=80, health_check=elbv2.HealthCheck(
            enabled=True,
            healthy_threshold_count=2,
            unhealthy_threshold_count=5,
            interval=Duration.seconds(30),
            timeout=Duration.seconds(5),
            path="/",
            port="8443"
        ))

        # add depends on for the listener to wait for the ec2 instance
        listener.node.add_dependency(ec2_instance)
        listener.node.add_dependency(ec2_instance2)