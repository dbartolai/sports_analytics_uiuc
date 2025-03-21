import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource("dynamodb", region_name="us-east-2")

try:
    tables = list(dynamodb.tables.all())
    print("Connected to DynamoDB. Tables found:", [table.name for table in tables])
except Exception as e:
    print("Error connecting to DynamoDB:", str(e))


class Weights:

    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource
        self.table = None

    def create_table(self, table_name):
        try:
            self.table = self.dyn_resource.create_table(
                Table_Name = table_name,
                KeySchema = [
                    {"AttributeName": "element", "KeyType": "HASH"}
                ],
                AttributeDefinitions = [
                    {"AttributeName": "element", "AttributeType": "S"}
                ],
                BillingMode = 'PAY_PER_REQUEST'
            )
            self.table.wait_until_exists()
        except ClientError as e:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                table_name,
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
            raise
        else:
            return self.table


    def add_weights(self, key, info):
        try:
            self.table.put_item(
                Item={
                    "Element" : key,
                    "Info" : info
                }
            )
        except ClientError as e:
            logger.error(
                "Couldn't add element %s to table %s. Here's why: %s: %s",
                key,
                self.table.name,
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
            raise

    def get_weights(self, key):
        try: response = self.table.get_item(Key={"element" : key})
        except ClientError as e:
            logger.error(
                "Couldn't get element %s from table %s. Here's why: %s: %s",
                key,
                self.table.name,
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
            raise
        else: return response["Info"]

    def update_weights(self, key, info):
        try:
            response = self.table.update_item(
                Key={"element": key},
                UpdateExpression="set Info = :info",
                ExpressionAttributeValues={":info": info},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            logger.error(
                "Couldn't update element %s in table %s. Here's why: %s: %s",
                key,
                self.table.name,
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
            raise
        else: return response["Attributes"]

