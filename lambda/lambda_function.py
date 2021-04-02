import boto3


def lambda_handler(event, context):
    print("------------------------")
    print(event)
    # 1. Iterate over each record
    try:
        for record in event["Records"]:
            # 2. Handle event by type
            if (
                record["eventName"] != "DELETE"
                and record["dynamodb"]["NewImage"]["state"]["S"] == "started"
            ):
                start_instance(record)
            elif (
                record["eventName"] != "DELETE"
                and record["dynamodb"]["NewImage"]["state"]["S"] == "stopped"
            ):
                stop_instance(record)
        print("------------------------")
        return "Success!"
    except Exception as e:
        print(e)
        print("------------------------")
        return "Error"


def start_instance(record):
    ec2_id = record["dynamodb"]["NewImage"]["ec2_id"]["S"]
    ec2_resource = boto3.resource("ec2")
    ec2_instance = ec2_resource.Instance(ec2_id)
    if record["dynamodb"]["NewImage"]["allowScheduling"]["BOOL"] == True:
        try:
            print("##########Tagging########")
            ec2_instance.create_tags(Tags=[{"Key": "scheduled", "Value": "true"}])
        except Exception as e:
            print(e)
    ec2_instance.start()
    print(f"EC2 instance with {ec2_id} started")


def stop_instance(record):
    ec2_id = record["dynamodb"]["NewImage"]["ec2_id"]["S"]
    ec2_resource = boto3.resource("ec2")
    ec2_instance = ec2_resource.Instance(ec2_id)
    if record["dynamodb"]["NewImage"]["allowScheduling"]["BOOL"] == False:
        try:
            print("##########Tagging########")
            ec2_instance.delete_tags(Tags=[{"Key": "scheduled", "Value": "true"}])
        except Exception as e:
            print(e)
    ec2_instance.stop()
    print(f"EC2 instance with {ec2_id} stopped")
