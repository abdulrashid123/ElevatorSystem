from django.db import models


STATUS_CHOICES = [
    ('idle', 'Idle'),
    ('moving_up', 'Moving Up'),
    ('moving_down', 'Moving Down'),
    ('door_open', 'Door Open'),
    ('stopped', 'Stopped'),
]

REQUEST_TYPE = [
    ('moving_up', 'Moving Up'),
    ('moving_down', 'Moving Down'),
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class System(BaseModel):
    name = models.CharField(max_length=200)


class Request(BaseModel):
    system = models.ForeignKey(System,on_delete=models.CASCADE,blank=True,null=True)
    floor = models.IntegerField()


class Elevator(BaseModel):
    system = models.ForeignKey(System,on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True)
    floor = models.IntegerField(default=0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Idle')
    is_running = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=False)
    # Add more fields as needed

    def move_up(self):
        # Logic to move the elevator up
        pass

    def move_down(self):
        # Logic to move the elevator down
        pass

    def open_door(self):
        # Logic to open the elevator door
        pass

    def close_door(self):
        # Logic to close the elevator door
        pass

    def start_running(self):
        self.is_running = True
        self.save()

    def stop_running(self):
        self.is_running = False
        self.save()

    def get_status(self):
        # Logic to retrieve and return the current status
        pass

    def decide_direction(self, requests):
        # Logic to decide whether to move up or down based on the requests
        pass



