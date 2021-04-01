from typing import List, NamedTuple

from marshmallow.schema import Schema
from marshmallow import fields, validate, ValidationError

from models.ec2_model import EC2ScheduleModel as ec2_m


class EC2Schema(Schema):
    """
    Schema for ec2 instances
    """
    ec2_id = fields.Str(required=True)
    schedule_days = fields.Int(required=True, validate=validate.Range([1,7]))
    last_state_change = fields.Date(dump_only=True, dump_to="lastStateChange")
    state = field.Str(dump_only=True)
    allow_scheduling = fields.Bool(dump_only=True, dump_to="allowScheduling")


class EC2SCollection(NamedTuple):
    ec2_instances: List[ec2_m]


class EC2CollectionSchema(Schema):
    ec2_instances = fields.List(fields.Nested(EC2Schema))


ec2_schema = EC2Schema()