import contextlib
from functools import wraps
from inspect import signature

import boto3


def provide_session(func):
    """
    Function decorator that provides a session if it isn't provided.
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        dynamodb = boto3.resource("dynamodb")
        session = dynamodb.Table("opslyft")
        return func(*args, session=session, **kwargs)
    return wrapper