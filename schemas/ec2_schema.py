from typing import List, NamedTuple

from marshmallow.schema import Schema
from marshmallow import fields, validate, ValidationError

from models.ec2_model import EC2ScheduleModel as ec2_m


class EC2Schema(Schema):
    """
    Schema for ec2 instances
    """
    ec2_id = fields.Str(required=True)
    schedule = fields.Int(validate=validate.Range(min=1,max=7))
    last_state_change = fields.Date(data_key="lastStateChange")
    state = fields.Str()
    allow_scheduling = fields.Bool(data_key="allowScheduling")


class EC2SCollection(NamedTuple):
    ec2_instances: List[ec2_m]


class EC2CollectionSchema(Schema):
    ec2_instances = fields.List(fields.Nested(EC2Schema))


ec2_schema = EC2Schema()