import os
import boto3

from .utils.session import provide_session


def ec2_dynamo_init():
    ec2_id_list = [for i in os.environ.get("EC2_LIST", None).split(" ")]
    if ec2_id_list != None:
        resource = boto3.resource{"dynamodb"}
        table = resource.Table("opslyft")

        for ec2_id in ec2_id_list:
            try:
                table.put_item(Item = {"ec2_id": ec2_id})
            except Exception as e:
                print(e)