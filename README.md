# Serverless AWS Instance Scheduler
The task was to create an API endpoint for scheduling an AWS EC2 instance using AWS Lambda. The endpoint takes JSON input from a user and can start and stop a user specified EC2 instance based on a schedule specified by the user.

## Implementation Overview
The architecture broadly contains 4 components.
 * CRUD based Flask REST API
 * Celery based monitor
 * DynamoDB as NoSQL database
 * AWS Lambda functions for carrying out the scheduling tasks
 
 The REST API and the celery monitor updates the entries in the dynamodb table depending upon the scenario. Any updates/insertions in the db creates a dynamodb stream which triggers the lamdba function. The triggered lambda function performs scheduling action on the updated ec2_schedule, i.e. starting, stopping and adding/removing tags on the ec2 instance.
 ![image info](./misc/arch.png)

