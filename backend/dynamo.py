import boto3
import logging
from botocore.exceptions import ClientError
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)



class Weights:

    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource
        self.table = None

    def create_table(self, table_name):
        try:
            self.table = self.dyn_resource.create_table(
                TableName = table_name,
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
        
    def use_table(self, table_name):
        self.table = self.dyn_resource.Table(table_name)


    def add_weights(self, key, info):
        try:
            self.table.put_item(
                Item={
                    "element" : key,
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

    def get_data(self, key):
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
        else: return response["Item"]["Info"]

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

    def delete_weights(self):
        try:
            self.table.delete()
            self.table = None
        except ClientError as e:
            logger.error(
                "Couldn't delete the table. Here's why: %s: %s",
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
            raise

def weight_data():
    file = open('weights.json')
    return json.load(file)
    
def delete_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
    weights = Weights(dynamodb)
    weights.use_table("Weights")
    weights.delete_weights()



def reset_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
    weights = Weights(dynamodb)
    weights.create_table("Weights")

    data = weight_data()
    print(data)

    weights.add_weights('W', data['W'])
    weights.add_weights('b', data['b'])
    weights.add_weights('V', data['V'])
    weights.add_weights('a', data['a'])

def get_weights():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
    weights = Weights(dynamodb)
    weights.use_table('Weights')

    data = {}

    data['W'] = weights.get_data('W')
    data['b'] = weights.get_data('b')
    data['V'] = weights.get_data('V')
    data['a'] = weights.get_data('a')

    return data

print(get_weights())
