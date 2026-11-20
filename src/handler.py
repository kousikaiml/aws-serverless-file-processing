import json, os
from datetime import datetime, timezone
from urllib.parse import unquote_plus
import boto3

s3=boto3.client("s3")
ddb=boto3.resource("dynamodb")

def process_record(record, table, output_bucket):
    event=json.loads(record["body"])
    output=[]
    for item in event.get("Records",[]):
        bucket=item["s3"]["bucket"]["name"]
        key=unquote_plus(item["s3"]["object"]["key"])
        head=s3.head_object(Bucket=bucket,Key=key)
        row={"objectKey":bucket+"/"+key,"sourceBucket":bucket,"sourceKey":key,
             "sizeBytes":head.get("ContentLength",0),
             "contentType":head.get("ContentType","application/octet-stream"),
             "processedAt":datetime.now(timezone.utc).isoformat(),"status":"PROCESSED"}
        table.put_item(Item=row)
        output_key="processed/"+key.rsplit("/",1)[-1]+".metadata.json"
        s3.put_object(Bucket=output_bucket,Key=output_key,
                      Body=json.dumps(row).encode(),ContentType="application/json")
        output.append(row)
    return output

def process_event(event, context):
    table=ddb.Table(os.environ["TABLE_NAME"])
    results=[]
    for record in event.get("Records",[]):
        results.extend(process_record(record,table,os.environ["OUTPUT_BUCKET"]))
    return {"processedCount":len(results),"items":results}
