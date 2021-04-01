from datetime import date

from utils.state_enums import State
class EC2ScheduleModel:
    """
    """
    def __init__(self, ec2_id, schedule, state=None, lastStateChange=None, toBeScheduled=None):
        self.ec2_id = ec2_id
        self.state = state
        self.lastStateChange = lastStateChange
        self.schedule = schedule
        self.toBeScheduled = toBeScheduled

    def add_defaults(self):
        """
        Add defautl arguemnts to a newly scheduled ec2 instance
        """
        self.lastStateChange = date.today()
        self.toBeScheduled = True
        self.state = State.STARTED

    def __str__(self):
        return f"{self.ec2_id} State: {self.state}"
        