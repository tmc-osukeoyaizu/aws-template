import json
import boto3

def main():
    client = boto3.client("iot-data")
    response = client.get_thing_shadow(thingName="lab2-mono", shadowName="")
    # StreamingBodyからデータを読み込む
    stream = response["payload"]
    shadow_payload = stream.read()

    # バイトデータをJSONにデコード
    shadow_data = json.loads(shadow_payload)

    # デコードされたデータを表示
    print(shadow_data)

if __name__ == "__main__":
    main()