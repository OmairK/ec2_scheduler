from datetime import date
from copy import deepcopy

from utils.state_enums import EC2State


def schedule_monitor(schedule):
    """
    Handles the routine case where there is no change in the schedule
    but the celery monitor might have to change the state depending upon the exisiting
    schedule of the instance
    """
    if schedule["state"] == EC2State.STOPPED:
        if (date.today() - schedule["lastStateChange"]).days >= 7 - schedule[
            "schedule"
        ]:
            schedule["state"] = EC2State.STARTED
    elif schedule["state"] == EC2State.STARTED:
        if (date.today() - schedule["lastStateChange"]).days >= schedule:
            schedule["state"] = EC2State.STOPPED
    else:
        return schedule, False

    return schedule, True
