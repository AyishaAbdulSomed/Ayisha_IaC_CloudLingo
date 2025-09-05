import boto3, json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    translate = boto3.client('translate')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(obj['Body'].read())

    result = translate.translate_text(
        Text=data['text'],
        SourceLanguageCode=data['source'],
        TargetLanguageCode=data['target']
    )

    output = {
        "original": data["text"],
        "translated": result["TranslatedText"]
    }

    s3.put_object(
        Bucket='iac-ayisha-response-bucket-kasi',
        Key=f"translated_{key}",
        Body=json.dumps(output)
    )
