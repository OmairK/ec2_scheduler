import boto3
from run import app
from flask import request
from botocore.exceptions import ClientError
from marshmallow import ValidationError

from models.ec2_model import EC2ScheduleModel
from utils.session import provide_session
from schemas.ec2_schema import ec2_schema


@app.route("/ec2/<id>", methods=["GET"])
@provide_session
def get_ec2(id, session):
    """
    Creates an ec2 instance
    :param id: The ec2 id.
    :return: The ec2 object with the specific id
    :rtype: object
    """
    try:
        response = session.get_item(Key={"ec2_id": id})
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 400
    else:
        return {"ec2_item": response["Item"]}, 200


@app.route("/ec2", methods=["POST"])
@provide_session
def create_ec2(session):
    """
    Creates an ec2 instance
    :return: The ec2 object with the specific id
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
    Updates the config of ec2 instance with the specific id
    :param id: The ec2 id.
    :return: The updated ec2 object
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
    Deletes the ec2 instance with the specified id
    :param id: The ec2 id.
    :return: message on successful deletion
    """
    try:
        ec2_json = session.get_item(Key={"ec2_id": id})
    except ClientError as e:
        return {"message": e.response["Error"]["Message"]}, 400

    ec2_object = EC2ScheduleModel(**ec2_schema.load(ec2_json["Item"]))
    update = ec2_object.delete_schedule()
    ec2_dump = ec2_schema.dump(ec2_object)

    if update:
        try:
            response = session.put_item(Item=ec2_dump)
            return {"message": "Resource deleted"}, 200
        except ClientError as e:
            return {"message": e.response["Error"]["Message"]}, 500
