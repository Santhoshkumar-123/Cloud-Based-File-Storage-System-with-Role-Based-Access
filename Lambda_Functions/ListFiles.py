import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("FileMetadata")

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "http://localhost:3000",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "OPTIONS,GET"
}


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


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

        if method != "GET":
            return {
                "statusCode": 405,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Method Not Allowed"})
            }

        role = get_user_role(event)
        claims = get_claims(event)
        user_id = claims.get("sub")

        # Visibility Rules
        if role in ["Admin", "Viewer"]:
            response = table.scan()
            items = response.get("Items", [])
        else:
            response = table.scan(
                FilterExpression=Attr("owner").eq(user_id)
            )
            items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(items, default=decimal_default)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }