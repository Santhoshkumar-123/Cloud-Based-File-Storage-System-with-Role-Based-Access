import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DownloadHistoryTable")

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "http://localhost:3000",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "OPTIONS,GET"
}


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def safe_int(value):
    try:
        return int(value)
    except:
        return 0


def lambda_handler(event, context):

    try:
        method = event.get("httpMethod")

        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": ""
            }

        if method != "GET":
            return {
                "statusCode": 405,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Method Not Allowed"})
            }

        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        user_id = claims.get("sub")

        if not user_id:
            raise Exception("User not authenticated")

        # Scan table (since we enabled Scan permission)
        response = table.scan()
        all_items = response.get("Items", [])

        # Filter only this user
        user_items = [
            item for item in all_items
            if item.get("userId") == user_id
        ]

        # 🔥 SAFE SORTING
        user_items = sorted(
            user_items,
            key=lambda x: safe_int(x.get("downloadedAt", 0)),
            reverse=True
        )

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(user_items, default=decimal_default)
        }

    except Exception as e:
        print("History Error:", str(e))
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }