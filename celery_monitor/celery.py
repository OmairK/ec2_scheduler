from celery import Celery
from celery.schedules import crontab

from utils.session import provide_session
from .controller import main_controller

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(minute=30, monitor.s(), name='monitor every 30 minutes')


@provide_session
def monitor(session):
    ec2_schedules_list = session.query(Select='ALL_ATTRIBUTES',KeyConditionExpression=Key('allowScheduling').eq(True))
    
    for ec2_schedule in ec2_schedules_list:
        schedule, update = main_controller(ec2_schedule, "Fixed")
        if update:
            ## Update logic
            # session.update_item
    
