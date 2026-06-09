import json
import boto3
import uuid
import time
from datetime import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

BUCKET_NAME = "cloud-file-storage-bucket-teamb"
TABLE_NAME = "FileMetadata"

table = dynamodb.Table(TABLE_NAME)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "http://localhost:3000",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}


def get_claims(event):
    return event.get("requestContext", {}) \
                .get("authorizer", {}) \
                .get("claims", {})


def get_user_role(event):
    claims = get_claims(event)
    groups = claims.get("cognito:groups", [])

    if isinstance(groups, str):
        groups = [groups]

    if "Admin" in groups:
        return "Admin"
    elif "Editor" in groups:
        return "Editor"
    else:
        return "Viewer"


def lambda_handler(event, context):

    try:
        method = event.get("httpMethod")

        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": ""
            }

        if method != "POST":
            return {
                "statusCode": 405,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Method Not Allowed"})
            }

        role = get_user_role(event)

        # Only Admin & Editor can upload
        if role not in ["Admin", "Editor"]:
            return {
                "statusCode": 403,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Access Denied"})
            }

        claims = get_claims(event)
        user_id = claims.get("sub")

        body = json.loads(event.get("body", "{}"))

        file_name = body.get("fileName")
        tags = body.get("tags", [])

        if not file_name:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "fileName is required"})
            }

        file_id = str(uuid.uuid4())
        s3_key = f"users/{user_id}/{file_name}"

        upload_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": s3_key,
                "ContentType": "application/octet-stream"
            },
            ExpiresIn=300
        )

        table.put_item(
            Item={
                "fileId": file_id,
                "owner": user_id,
                "fileName": file_name,
                "s3Key": s3_key,
                "tags": tags,
                "uploadTime": int(time.time()),
                "uploadedAt": datetime.utcnow().isoformat(),
                "uploadedByRole": role
            }
        )

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "uploadUrl": upload_url,
                "fileId": file_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }