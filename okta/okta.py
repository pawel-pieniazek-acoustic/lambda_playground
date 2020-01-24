import logging

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    url = "https://acoustic.oktapreview.com/oauth2/ausp5s1p9r1FIHgnv0h7/v1/token?grant_type=client_credentials&scope=tenant_id"

    payload = {}
    files = {}
    headers = {
        'Authorization': 'Basic MG9hcDV3Mmd5cXVyODZqT0YwaDc6dHgwVUVBUUZJdjJVS3planVubG5jRTl4Z0JnNm4yZTFUZW82YURINw==',
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text.encode('utf8'))
