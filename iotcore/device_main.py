# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import
from __future__ import print_function

import argparse
import json
import logging
import os
import random
import signal
import sys
import time
import traceback
from datetime import datetime

from awscrt import io, mqtt
from awsiot import iotshadow, mqtt_connection_builder

# - Overview -
# This sample shows 1) how to connect AWS IoT Core. 2) How to use AWS IoT
# Device Shadow

BASE_TOPIC = "data/"
DEFAULT_WAIT_TIME = 5
SHADOW_WAIT_TIME_KEY = "wait_time"
KEEP_ALIVE = 300

mqtt_connection = None
shadow_client = None
wait_time = DEFAULT_WAIT_TIME
device_name = None

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.basicConfig()


def arg_check():
    """
    argument check
    """

    logging.debug("start: arg_check")
    parser = argparse.ArgumentParser()
    parser.add_argument("--device_name", required=True,
                        help="[Must], AWS IoT Core Thing Name")
    parser.add_argument("--endpoint", required=True,
                        help="[Must], AWS IoT endpoint URI")

    #コマンド実行時にメッセージ追加
    parser.add_argument("--message", required=False,
                        help="send message")
    parser.add_argument("--root_ca", required=False,
                        help="AWS IoT Core root ca file name with path")
    parser.add_argument("--cert", required=False,
                        help="device cert file name with path")
    parser.add_argument("--private", required=False,
                        help="private cert key file name with path")
    parser.add_argument('--verbosity', choices=[x.name for x in io.LogLevel],
                        default=io.LogLevel.NoLogs.name, help='Logging level')

    args = parser.parse_args()

    log_level = getattr(io.LogLevel, args.verbosity, "error")
    io.init_logging(log_level, 'stderr')
    loglevel_map = [
        logging.INFO, logging.INFO, logging.INFO,
        logging.INFO, logging.INFO, logging.DEBUG,
        logging.DEBUG]
    logger.setLevel(loglevel_map[log_level])
    logging.basicConfig()

    cert_list = find_certs_file()
    if args.root_ca is not None:
        cert_list[0] = args.root_ca
    if args.private is not None:
        cert_list[1] = args.private
    if args.cert is not None:
        cert_list[2] = args.cert

    logging.debug(cert_list)
    file_exist_check(cert_list)

    init_dict = {
    init_info = arg_check()
    device_name = init_info['device_name']
    iot_endpoint = init_info['endpoint']

    #コマンド実行時にメッセージ追加
    message = init_info['message']


    rootca_file = init_info['certs'][0]
    private_key_file = init_info['certs'][1]
    certificate_file = init_info['certs'][2]

    logger.info("device_name: %s", device_name)
    logger.info("endpoint: %s", iot_endpoint)
    logger.info("rootca cert: %s", rootca_file)
    logger.info("private key: %s", private_key_file)
    logger.info("certificate: %s", certificate_file)

    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=iot_endpoint,
        cert_filepath=certificate_file,
        pri_key_filepath=private_key_file,
        client_bootstrap=client_bootstrap,
        ca_filepath=rootca_file,
        client_id=device_name,
        clean_session=False,
        keep_alive_secs=KEEP_ALIVE)

    connected_future = mqtt_connection.connect()
    shadow_client = iotshadow.IotShadowClient(mqtt_connection)
    connected_future.result()

    print("Check latest Shadow status")
    get_accepted_subscribed_future, _ = shadow_client.subscribe_to_get_shadow_accepted(
        request=iotshadow.GetShadowSubscriptionRequest(device_name),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_get_shadow_accepted)

    get_rejected_subscribed_future, _ = shadow_client.subscribe_to_get_shadow_rejected(
        request=iotshadow.GetShadowSubscriptionRequest(device_name),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_get_shadow_rejected)

    # Wait for subscriptions to succeed
    get_accepted_subscribed_future.result()
    get_rejected_subscribed_future.result()

    publish_get_future = shadow_client.publish_get_shadow(
        request=iotshadow.GetShadowRequest(device_name),
        qos=mqtt.QoS.AT_LEAST_ONCE)

    # Ensure that publish succeeds
    publish_get_future.result()

    logger.info("Subscribing to Shadow Delta events...")
    delta_subscribed_future, _ = shadow_client.subscribe_to_shadow_delta_updated_events(
        request=iotshadow.ShadowDeltaUpdatedSubscriptionRequest(device_name),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_shadow_delta_updated)

    # Wait for subscription to succeed
    delta_subscribed_future.result()

    logger.info("Subscribing to Shadow Update responses...")
    update_accepted_subscribed_future, _ = shadow_client.subscribe_to_update_shadow_accepted(
        request=iotshadow.UpdateShadowSubscriptionRequest(device_name),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_update_shadow_accepted)

    update_rejected_subscribed_future, _ = shadow_client.subscribe_to_update_shadow_rejected(
        request=iotshadow.UpdateShadowSubscriptionRequest(device_name),
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_update_shadow_rejected)

    # Wait for subscriptions to succeed
    update_accepted_subscribed_future.result()
    update_rejected_subscribed_future.result()

    # Start sending dummy data
    topic = BASE_TOPIC + device_name
    logging.info("topic: %s", topic)
    while True:
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        tmp = 20 + random.randint(-5, 5)
        hum = 50 + random.randint(-10, 10)
        payload = {"DEVICE_NAME": device_name, "TIMESTAMP": now, "TEMPERATURE": tmp, "HUMIDITY": hum, "MESSAGE": message} #コマンド実行時にメッセージ追加
        logger.debug("  payload: %s", payload)

        mqtt_connection.publish(
            topic=topic,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE)

        time.sleep(wait_time)


def exit_sample(msg_or_exception):
    """
    Exit sample with cleaning

    Parameters
    ----------
    msg_or_exception: str or Exception
    """
    if isinstance(msg_or_exception, Exception):
        logger.error("Exiting sample due to exception.")
        traceback.print_exception(msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2])
    else:
        logger.info("Exiting: %s", msg_or_exception)

    if not mqtt_connection:
        logger.info("Disconnecting...")
        mqtt_connection.disconnect()
    sys.exit(0)


def exit_handler(_signal, frame):
    """
    Exit sample
    """
    exit_sample(" Key abort")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)

    device_main()