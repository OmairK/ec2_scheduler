import os
import boto3


def ec2_dynamo_init():
    ec2_id_list = os.environ.get("EC2_LIST", None)
    if ec2_id_list != None:
        ec2_id_list = [str(i) for i in ec2_id_list.split(" ")]
        resource = boto3.resource("dynamodb")
        table = resource.Table("opslyft")

        for ec2_id in ec2_id_list:
            try:
                table.put_item(Item = {"ec2_id": ec2_id})
            except Exception as e:
                print(e)