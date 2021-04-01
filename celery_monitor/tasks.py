import boto3
from celery import Celery
from celery.schedules import crontab
from datetime import date

from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

app = Celery("tasks")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, monitor.s(), name="monitor every 10 seconds")


@app.task
def monitor():
    ec2_schedules_list = (
        boto3.resource("dynamodb")
        .Table("opslyft")
        .scan(FilterExpression=Key("allowScheduling").eq(True))
    )
    print(ec2_schedules_list)
    for ec2_schedule in ec2_schedules_list["Items"]:
        schedule, update = schedule_monitor(ec2_schedule)
        if update:
            boto3.resource("dynamodb").Table("opslyft").put_item(Item=schedule)


def schedule_monitor(schedule):
    """
    Handles the routine case where there is no change in the schedule
    but the celery monitor might have to change the state depending upon the exisiting
    schedule of the instance
    """
    if schedule["state"] == "stopped":
        if (date.today() - datetime.strptime(schedule["lastStateChange"], '%Y-%d-%m').date()).days >= 7 - int(schedule["schedule"]):
            schedule["state"] = "started"
            schedule["lastStateChange"] = str(date.today())
    elif schedule["state"] == "started":
        if (date.today() - datetime.strptime(schedule["lastStateChange"], '%Y-%d-%m').date()).days >= int(schedule["schedule"]):
            schedule["state"] = "stopped"
            schedule["lastStateChange"] = str(date.today())
    else:
        return schedule, False

    return schedule, True