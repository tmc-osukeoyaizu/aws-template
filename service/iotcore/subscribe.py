from awscrt import io, mqtt
from awsiot import mqtt_connection_builder, iotshadow
import threading

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


#イベントが発生する度に実行される関数
def on_update_shadow_accepted(response: iotshadow.UpdateShadowResponse):
    print("Shadow Update Accepted:")
    print(response.state)


def on_shadow_update_rejected(error):
    print("Shadow Update Rejected:")
    print(error)

def on_get_shadow_accepted(response: iotshadow.GetShadowResponse):
    print("Shadow Get Accepted:")
    print(response.state)


def on_shadow_get_rejected(error):
    print("Shadow Get Rejected:")
    print(error)


def main():
    mqtt_connection = mqtt_connect()
    shadow = iotshadow.IotShadowClient(mqtt_connection)

    # Updateの成功をサブスクライブする
    update_accepted_future, _ = shadow.subscribe_to_update_named_shadow_accepted(
        request=iotshadow.UpdateNamedShadowSubscriptionRequest(
            thing_name="lab2-mono",
            shadow_name="lab2_Shadow",
        ),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_update_shadow_accepted,
    )
    update_accepted_future.result()

    # Updateの失敗をサブスクライブする
    update_rejected_future, _ = shadow.subscribe_to_update_named_shadow_rejected(
        request=iotshadow.UpdateNamedShadowSubscriptionRequest(
            thing_name="lab2-mono",
            shadow_name="lab2_Shadow",
        ),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_shadow_update_rejected,
    )
    update_rejected_future.result()

    # Getの成功をサブスクライブする
    get_accepted_future, _ = shadow.subscribe_to_get_named_shadow_accepted(
        request=iotshadow.GetNamedShadowSubscriptionRequest(
            thing_name="lab2-mono",
            shadow_name="lab2_Shadow",
        ),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_get_shadow_accepted,
    )
    get_accepted_future.result()

    # Getの失敗をサブスクライブする
    get_rejected_future, _ = shadow.subscribe_to_get_named_shadow_rejected(
        request=iotshadow.GetNamedShadowSubscriptionRequest(
            thing_name="lab2-mono",
            shadow_name="lab2_Shadow",
        ),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_shadow_get_rejected,
    )
    get_rejected_future.result()

    print("Waiting for shadow publish...")
    try:
        threading.Event().wait()
    finally:
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()

if __name__ == "__main__":
    main()