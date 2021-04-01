from typing import List, NamedTuple

from marshmallow.schema import Schema
from marshmallow import fields, validate, ValidationError

class EC2Schema(Schema):
    """
    Schema for ec2 instances
    """
    ec2_id = fields.Str()
    schedule_days = fields.Int()

class EC2SCollection(NamedTuple):
    ec2_instances: List[EC2Instances]

class EC2CollectionSchema(Schema):
    ec2_instances = fields.List(fields.Nested(EC2Schema))

ec2_schema = EC2Schema()