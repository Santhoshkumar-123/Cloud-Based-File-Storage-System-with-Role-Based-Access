import json
import boto3

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

BUCKET_NAME = "cloud-file-storage-bucket-teamb"
TABLE_NAME = "FileMetadata"

table = dynamodb.Table(TABLE_NAME)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "http://localhost:3000",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "OPTIONS,DELETE"
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

        # Handle CORS preflight
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": ""
            }

        if method != "DELETE":
            return {
                "statusCode": 405,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Method Not Allowed"})
            }

        role = get_user_role(event)

        # 🔐 Only Admin can delete
        if role != "Admin":
            return {
                "statusCode": 403,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Only Admin can delete files"})
            }

        body = json.loads(event.get("body", "{}"))
        file_id = body.get("fileId")

        if not file_id:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "fileId is required"})
            }

        # Get file metadata
        response = table.get_item(Key={"fileId": file_id})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "File not found"})
            }

        file_item = response["Item"]

        # Delete file from S3
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=file_item["s3Key"]
        )

        # Delete metadata from DynamoDB
        table.delete_item(Key={"fileId": file_id})

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": "File deleted successfully"})
        }

    except Exception as e:
        print("Delete Error:", str(e))
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }