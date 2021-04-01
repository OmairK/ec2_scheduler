import json

import boto3
print('Loading function')

def lambda_handler(event, context):
	print('------------------------')
	print(event)
	#1. Iterate over each record
	try:
		for record in event['Records']:
			#2. Handle event by type
			if record['dynamodb']['state'] == 'up':
				start_instance(record)
			elif record['dynamodb']['state'] == 'down':
				stop_instance(record)
		print('------------------------')
		return "Success!"
	except Exception as e: 
		print(e)
		print('------------------------')
		return "Error"


def start_instance(record):
	ec2_id = record['dynamodb']['ec2_id']
    ec2_resource = boto3.resource("ec2")
    #TODO: Error handling in case of wrong ec2 instance
    ec2_instance = ec2_resource.Instance(ec2_id)
    ec2_instance.start()
	print(f'EC2 instance with {ec2_id} started')


def handle_modify(record):
	ec2_id = record['dynamodb']['ec2_id']
    ec2_resource = boto3.resource("ec2")
    #TODO: Error handling in case of wrong ec2 instance
    ec2_instance = ec2_resource.Instance(ec2_id)
    ec2_instance.stop()
	print(f'EC2 instance with {ec2_id} stopped')