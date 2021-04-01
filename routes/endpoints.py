import boto3
from run import app
from flask import request
from botocore.exceptions import ClientError

from utils.session import provide_session
from schemas.ec2_schema import ec2_schema

@app.route("/ec2/<id>", methods=['GET'])
@provide_session
def get_ec2(id, session):
    """
    Creates an ec2 instance
    :param id: The ec2 id.
    :return: The ec2 object with the specific id
    :rtype: object
    """
    try:
        response = session.get_item(Key={'ec2_id': id})
    except ClientError as e:
        return {"message": e.response['Error']['Message']}, 400
    else:
        return {"ec2_item": response['Item']},200

@provide_session
@app.route("/ec2", methods=['POST'])
def create_ec2(session):
    """
    Creates an ec2 instance
    :return: The ec2 object with the specific id
    """
    # Marshmallow serialization
    try:
        body = ec2_schema.load(request.json)
    except ValidationError as err:
        return {"message": str(err.messages)}, 400
    response = session.put_item()
    return 


@provide_session
@app.route("/ec2/<id>", methods=['PUT'])
def patch_ec2(id, session):
    """
    Updates the config of ec2 instance with the specific id
    :param id: The ec2 id.
    :return: The updated ec2 object
    """
    if id != request.json["ec2_id"]:
        return {"message": "The id doesnt match the payload"},400
    try:
        body = ec2_schema.load(request.json)
    except ValidationError as err:
        return {"message": str(err.messages)}, 400
    
    try:
        ec2_schema = session.get_item(Key={'ec2_id': id})
    except ClientError as e:
        return {"message": e.response['Error']['Message']}, 400
    
    response = session.update_item(Key={"ec2_instance": id}, AttributeUpdates=body)
    return {"data": course_schema.dump(course)}, 200 

    
    

@provide_session
@app.route("/ec2/<id>", methods=['DELETE'])
def delete_ec2(id, session):
    """
    Deletes the ec2 instance with the specified id
    :param id: The ec2 id.
    :return: message on successful deletion
    """
    try:
        response = session.delete_item(Key={"ec2_id": id})
    except ClientError as e:
        return {"message": e.response['Error']['Message']}, 400
    else:
        return {"message": "Resource deleted"},200
    