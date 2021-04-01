import contextlib
from functools import wraps
from inspect import signature

import boto3



@contextlib.contextmanager
def create_session():
    """Contextmanager that will create and teardown a session."""
    dynamodb = boto3.resource("dynamodb")
    session = dynamodb.Table("opslyft")


def provide_session(func):
    """
    Function decorator that provides a session if it isn't provided.
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> RT:
        if "session" in kwargs or :
            return func(*args, **kwargs)
        else:
            with create_session() as session:
                return func(*args, session=session, **kwargs)

    return wrapper