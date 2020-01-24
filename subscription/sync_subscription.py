import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def add_tenant_info(input_json):
    """Should add the customer and admin user to Okta and also call the new
    tenantid service with the full json

    If either already exists, should just use them.  this function could be common in all 7 lamda microservices

    should return updated json, with that data added to the json.
   """

    tenant_id = 12132321214  # replace hardcoded with call to service to create tenant if not exist otherwise return tenantid
    acoustic_id = 23423423234  # replace hardcodedwith call to okta to create customer if not exist, otherwise return customer

    new_json = input_json
    new_json["tenantid"] = tenant_id  # this will append that data to the json using the new key
    new_json["acoustic_id"] = acoustic_id  # this will append that data to the json using the new key

    return new_json


def lambda_handler(event, context):
    logger.info("input event %s", event)

    return {
        "statusCode": 200,
        "body": json.dumps('success handling sync customer')
    }
