from datetime import date

from utils.state_enums import State, EC2State

class EC2ScheduleModel:
    """
    Proxy model for preprocessing.
    Could be used for plugging in an ORM
    """
    def __init__(self, ec2_id, schedule=None, state=None, last_state_change=None, allow_scheduling=None):
        self.ec2_id = ec2_id
        self.state = state
        self.last_state_change = last_state_change
        self.schedule = schedule
        self.toBeScheduled = allow_scheduling

    def add_defaults(self):
        """
        Add defautl arguemnts to a newly scheduled ec2 instance
        """
        self.last_state_change = date.today()
        self.allow_scheduling = True
        self.state = EC2State.STARTED
    
    def validate_ec2_instance(self):
        import boto3
        ec2_resource = boto3.resource("ec2")
        ec2_instance = ec2_resource.Instance(self.ec2_id)

        try:
            _ = ec2_instance.state
            return True
        except Exception:
            return False

    def delete_schedule(self):
        """
        Handles the case where the schedule of an ec2 is deleted
        """
        if self.state == EC2State.STOPPED and self.allow_scheduling == False:
            return False
        
        self.state = EC2State.STOPPED
        self.allow_scheduling = False
        self.schedule = None
        self.last_state_change = date.today()
        return True

    def update_schedule(self, new_schedule):
        """
        Handles the case where the schedule of an ec2 instance is updated
        """
        if self.state == EC2State.STARTED and (self.schedule > new_schedule):
            self.allow_scheduling = True
            self.state = EC2State.STOPPED
            self.schedule = new_schedule
            return True
            
        elif self.state == EC2State.STOPPED and (self.schedule < new_schedule):
            self.state = EC2State.STARTED
            self.allow_scheduling = True
            self.schedule = new_schedule
            return True

        return False

    def __str__(self):
        return f"{self.ec2_id} State: {self.state}"
        