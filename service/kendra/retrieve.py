import boto3
import json
import pprint
kendra = boto3.client('kendra')
def lambda_handler(event, context):
    # クエリのテキストをハードコーディング(検索内容を記載)
    query_text = 'IP'
    # Kendra インデックス ID に置き換え
    index_id = '96fb7d0a-45f6-4e45-b93e-e8fd741d4d33'  
    response = kendra.retrieve(
        QueryText=query_text,
        IndexId=index_id,
        AttributeFilter={
            "EqualsTo": {
                "Key": "_language_code",
                "Value": {"StringValue": "ja"},
            },
        },
    )
    print(response)
    # Kendra の応答から最初の3つの結果を抽出
    results = response['ResultItems'][:3] if response['ResultItems'] else []
    results_list = {}
    index = 0
    for item in response['ResultItems']:
        result_item = {
            'Content': item['Content'],
            'DocumentURI': item['DocumentURI'],
        }
        index = index + 1
        results_list[index] = result_item
    pprint.pprint(results_list)
    print(results_list)
    
    extracted_results = []
    for item in results:
        content = item.get('Content')
        document_uri = item.get('DocumentURI')
        extracted_results.append({
            'Content': content,
            'DocumentURI': document_uri,
        })
    print("Kendra extracted_results:" + json.dumps(extracted_results, ensure_ascii=False))
    return extracted_results