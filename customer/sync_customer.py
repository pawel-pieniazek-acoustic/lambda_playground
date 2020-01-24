import datetime
import json
import logging
import os

import boto3
import requests
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    logging.info("creating bucket %s, %s", bucket_name, region)
    # Create bucket
    bucket = None

    try:
        if region is None:
            s3_client = boto3.client('s3')

            bucket = s3_client.create_bucket(Bucket=bucket_name)

        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            bucket = s3_client.create_bucket(Bucket=bucket_name,
                                             CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)

    return bucket


def add_tenant_info(input_json):
    """Should add the customer and admin user to Okta and also call the new
    tenantid service with the full json

    If either already exists, should just use them.  this function could be common in all 7 lamda microservices

    should return updated json, with that data added to the json.
   """

    os.environ.setdefault('okta_url',
                          'https://acoustic.oktapreview.com/oauth2/ausp5s1p9r1FIHgnv0h7/v1/token?grant_type=client_credentials&scope=tenant_id')
    os.environ.setdefault('basic_key',
                          'MG9hcDV3Mmd5cXVyODZqT0YwaDc6dHgwVUVBUUZJdjJVS3planVubG5jRTl4Z0JnNm4yZTFUZW82YURINw==')

    okta_url = os.environ.get("okta_url")
    basic_key = os.environ.get("basic_key")
    resp = requests.post(okta_url, json={}, headers={'Authorization': 'Basic ' + basic_key})
    if resp.status_code != 201:
        raise Exception('POST /tasks/ {}'.format(resp.status_code))

    access_token = resp.json()["access_token"]
    print('Retrieved Token: {}'.format(access_token))

    tenant_id = 12132321214  # replace hardcoded with call to service to create tenant if not exist otherwise return tenantid
    acoustic_id = 23423423234  # replace hardcodedwith call to okta to create customer if not exist, otherwise return customer

    new_json = input_json
    new_json["tenant_id"] = tenant_id  # this will append that data to the json using the new key
    new_json["acoustic_id"] = acoustic_id  # this will append that data to the json using the new key

    return new_json


def sync_customer(event, context):
    logger.info("input event %s", event)
    s3_client = boto3.resource('s3')
    bucket_name = os.environ.get("bucket_name")
    product_bucket = create_bucket(bucket_name,
                                   'us-east-2')  # create is idempotent, so if not exist it will create, if exist it returns it
    logger.info("returned bucket %s", product_bucket)

    new_json = add_tenant_info(event)  # add our tenantid and acousticid info to the json from salesforce

    filename = 'SyncCustomer_' + str(
        datetime.datetime.now()) + '.json'  # each call to provisioning api, should be independent

    s3object = s3_client.Object(bucket_name, filename)

    json_as_string = json.dumps(new_json)
    s3object.put(Body=(bytes(json_as_string.encode('UTF-8'))))

    logger.info("stored file with key %s", filename)

    return {
        "statusCode": 200,
        "body": json.dumps('success handling sync customer')
    }
