from typing import List, NamedTuple

from marshmallow import ValidationError, fields, validate
from marshmallow.schema import Schema

from models.ec2_model import EC2ScheduleModel as ec2_m


class EC2Schema(Schema):
    """
    Schema for ec2 instances
    """

    ec2_id = fields.Str(required=True)
    schedule = fields.Int(validate=validate.Range(min=1, max=7))
    last_state_change = fields.Date(data_key="lastStateChange")
    state = fields.Str()
    allow_scheduling = fields.Bool(data_key="allowScheduling")


class EC2DynamoSchema(Schema):
    """
    Schema for ec2 instances dynamo objects
    """

    ec2_id = fields.Str(required=True)
    schedule = fields.Int(validate=validate.Range(min=1, max=7))
    lastStateChange = fields.Str()
    state = fields.Str()
    allowScheduling = fields.Str()


class EC2SCollection(NamedTuple):
    ec2_instances: List


class EC2CollectionSchema(Schema):
    ec2_instances = fields.List(fields.Nested(EC2DynamoSchema))


ec2_schema = EC2Schema()
ec2_collection_schema = EC2CollectionSchema()
ec2_dynamo_schema = EC2DynamoSchema()
