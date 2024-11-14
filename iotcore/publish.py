from awscrt import io, mqtt
from awsiot import mqtt_connection_builder, iotshadow

def mqtt_connect() -> mqtt.Connection:
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint="aw61t711eg2co-ats.iot.ap-northeast-1.amazonaws.com",
        cert_filepath="./certs/7fa62d761047783cdaad5ce760de0616c31f4034dcfda5a2fdf2f9651d5eafac-certificate.pem.crt",
        pri_key_filepath="./certs/7fa62d761047783cdaad5ce760de0616c31f4034dcfda5a2fdf2f9651d5eafac-private.pem.key",
        ca_filepath="./certs/AmazonRootCA1.pem",
        client_bootstrap=client_bootstrap,
        client_id="client_id",
        clean_session=False,
        keep_alive_secs=6,
    )
    connected_future = mqtt_connection.connect()
    connected_future.result()

    return mqtt_connection

def main():
    mqtt_connection = mqtt_connect()
    shadow = iotshadow.IotShadowClient(mqtt_connection)

    # Updateを送信する
    update_shadow_future = shadow.publish_update_named_shadow(
        request=iotshadow.UpdateNamedShadowRequest(
            thing_name="lab2-mono",
            shadow_name="lab2_Shadow",
            state=iotshadow.ShadowState(
                # デバイスの現在の状態
                reported=None,
                reported_is_nullable=True,
                # デバイスが達成すべき目標の状態
                desired={
                    "settings": {
                        "mode": 1,
                        "temp": 20,
                    },
                    "firmware_url": "https://s3.com/firmware.bin",
                },
                desired_is_nullable=True,
                # reportedとdesiredの差分
                # delta=None,
                # delta_is_nullable=True,
            ),
        ),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )
    update_shadow_future.result()

    # Getを送信する
    get_shadow_future = shadow.publish_get_named_shadow(
        request=iotshadow.GetNamedShadowRequest(
            thing_name="Test-Device",
            shadow_name="test1",
        ),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )
    get_shadow_future.result()

    print("Publish Complete!")

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

if __name__ == "__main__":
    main()