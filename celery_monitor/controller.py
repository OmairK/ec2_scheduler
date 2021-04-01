from datetime import date
from copy import deepcopy


def main_controller(ec2_object, schedule_state, new_schedule=None):
    """
    Main controller that handles the delegation of schedule updation
    task to other functions
    :return: Tuple containing the schedule and the bool if the schedule has
     updated or not
    :rtype: Tuple
    """
    if schedule_state == "Deleted":
        return deleted_schedule(ec2_object)
    elif schedule_state == "Updated":
        return updated_schedule(ec2_object, new_schedule)
    else:
        return fixed_schedule(ec2_object)


def deleted_schedule(old_schedule):
    """
    Handles the case where the schedule of an ec2 is deleted
    """
    new_schedule = deepcopy(old_schedule)
    new_schedule["state"] = "down"
    new_schedule["allowScheduling"] = False
    new_schedule["schedule"] = None
    new_schedule["lastStateChange"] = str(date.today())
    return new_schedule, True


def updated_schedule(old_schedule, new_schedule):
    """
    Handles the case where the schedule of an ec2 instance is updated
    """
    if old_schedule["state"] == "up":
        pass
    elif old_schedule["state"] == "down":
        pass


def fixed_schedule(schedule):
    """
    Handles the routine case where there is no change in the schedule
    but the celery monitor might have to change the state depending upon the exisiting
    schedule of the instance
    """
    if schedule["state"] == "down":
        if (date.today() - schedule["lastStateChange"]).days >= 7 - schedule[
            "schedule"
        ]:
            schedule["state"] = "up"
    elif schedule["state"] == "up":
        if (date.today() - schedule["lastStateChage"]).days >= schedule:
            schedule["state"] = "down"
    else:
        return schedule, False

    return schedule, True