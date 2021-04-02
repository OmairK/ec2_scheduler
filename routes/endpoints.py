import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import request
from botocore.exceptions import ClientError
from marshmallow import ValidationError
from flasgger import swag_from

from models.ec2_model import EC2ScheduleModel
from utils.session import provide_session
from schemas.ec2_schema import (
    ec2_schema,
    ec2_collection_schema,
    EC2SCollection,
    ec2_dynamo_schema,
)

from main import app


@app.route("/")
def hello_world():
    """
    Health Check endpoint
    ---
    responses:
      200:
        description: Health check hello world
        schema:
          id: message
          type: string
    """
    return {"message": "Hello World"}, 200


@app.route("/ec2/all", methods=["GET"])
@provide_session
def get_ec2s(session):
    """
    Creates schedule for a valid ec2 instance
    ---
    definitions:
      - ec2_item:
          type: object
          properties:
            ec2_id:
              type: string
            schedule:
              type: integer
            state:
              type: string
            lastStateChange:
              type: string
            allowScheduling:
              type: boolean
    responses:
      200:
        description: Returns the schedule of ec2 with the given id
        schema:
          type: object
          properties:
            ec2_instances:
              type: array
              items:
                $ref: '#/definitions/ec2_item'
    """
    try:
        ec2_list = session.scan(FilterExpression=Key("allowScheduling").eq(True))
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 500
    return (
        ec2_collection_schema.dumps(EC2SCollection(ec2_instances=ec2_list["Items"])),
        200,
    )


@app.route("/ec2/<id>", methods=["GET"])
@provide_session
def get_ec2(id, session):
    """
    Gets an ec2 instance schedule
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    definitions:
      - ec2_item:
          type: object
          properties:
            ec2_id:
              type: string
            schedule:
              type: integer
            state:
              type: string
            lastStateChange:
              type: string
            allowScheduling:
              type: boolean
    responses:
      200:
        description: Returns the schedule of ec2 with the given id
        schema:
          $ref: '#/definitions/ec2_item'
    """
    try:
        response = session.get_item(Key={"ec2_id": id})
        response["Item"]["schedule"] = int(response["Item"]["schedule"])
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 500
    else:
        return {"ec2_item": response["Item"]}, 200


@app.route("/ec2", methods=["POST"])
@provide_session
def create_ec2(session):
    """
    Creates schedule for a valid ec2 instance
    ---
    parameters:

      - name: body
        in: body
        required: true
        type: string
        schema:
            id : create_ec2
            required:
              - ec2_id
              - schedule
            properties:
              ec2_id:
                type: string
                description: Unique identifier representing an ec2 instance
              schedule:
                type: integer
                description: Schedule for the ec2 instance

    definitions:
      - ec2_item:
          type: object
          properties:
            ec2_id:
              type: string
            schedule:
              type: integer
            state:
              type: string
            lastStateChange:
              type: string
            allowScheduling:
              type: boolean
    responses:
      200:
        description: Returns the schedule of ec2 with the given id
        schema:
          $ref: '#/definitions/ec2_item'

    """

    try:
        body = ec2_schema.load(request.json)
    except ValidationError as err:
        return {"message": str(err.messages)}, 400

    ec2_m = EC2ScheduleModel(body["ec2_id"], body["schedule"])

    if ec2_m.validate_ec2_instance() == False:
        return {"message": f"No such ec2 resource with id: {ec2_m.ec2_id} present"}, 400

    ec2_m.add_defaults()
    ec2_json = ec2_schema.dump(ec2_m)
    try:
        response = session.put_item(Item=ec2_json)
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 500

    return ec2_json, 200


@app.route("/ec2/<id>", methods=["PUT"])
@provide_session
def patch_ec2(id, session):
    """
    Updates schedule of an ec2 instance
    ---
    parameters:
      - name: body
        in: body
        required: true
        type: string
        schema:
            id : update_ec2
            required:
              - ec2_id
              - schedule
            properties:
              ec2_id:
                type: string
                description: Unique identifier representing an ec2 instance
              schedule:
                type: integer
                description: Schedule for the ec2 instance
      - name: id
        in: path
        required: true
        type: string

    definitions:
      - ec2_item:
          type: object
          properties:
            ec2_id:
              type: string
            schedule:
              type: integer
            state:
              type: string
            lastStateChange:
              type: string
            allowScheduling:
              type: boolean
    responses:
      200:
        description: Returns the schedule of ec2 with the given id
        schema:
          $ref: '#/definitions/ec2_item'

    """
    if id != request.json["ec2_id"]:
        return {"message": "The id doesnt match the payload"}, 400

    try:
        body = ec2_schema.load(request.json)
    except ValidationError as err:
        return {"message": str(err.messages)}, 400

    try:
        ec2_json = session.get_item(Key={"ec2_id": id})
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 400

    ec2_json["Item"]["schedule"] = 1
    ec2_object = EC2ScheduleModel(**ec2_schema.load(ec2_json["Item"]))
    update = ec2_object.update_schedule(body["schedule"])
    ec2_dump = ec2_schema.dump(ec2_object)

    if update:
        try:
            response = session.put_item(Item=ec2_dump)
            return ec2_schema.dump(ec2_object), 200
        except ClientError as e:
            return {"message": e.response["Error"]["Message"]}, 500
    else:
        return ec2_schema.dump(ec2_object), 200


@app.route("/ec2/<id>", methods=["DELETE"])
@provide_session
def delete_ec2(id, session):
    """
    Deletes the schedule of an ec2 instance with the specified id
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    definitions:
      - message:
          type: string
    responses:
      200:
        description: Returns the schedule of ec2 with the given id
        schema:
          $ref: '#/definitions/message'
    """
    try:
        ec2_json = session.get_item(Key={"ec2_id": id})
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 400

    ec2_json["Item"].pop("schedule")
    ec2_object = EC2ScheduleModel(**ec2_schema.load(ec2_json["Item"]))
    update = ec2_object.delete_schedule()
    ec2_dump = ec2_schema.dump(ec2_object)

    if update:
        try:
            response = session.put_item(Item=ec2_dump)
            return {"message": "Resource deleted"}, 200
        except ClientError as e:
            return {"message": e.response["Error"]["Message"]}, 500
