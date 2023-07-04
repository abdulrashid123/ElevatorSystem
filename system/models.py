from django.db import models


STATUS_CHOICES = [
    ('IDLE', 'IDLE'),
    ('MOVING UP', 'MOVING UP'),
    ('MOVING DOWN', 'MOVING DOWN'),
    ('DOOR OPEN', 'DOOR OPEN'),
    ('DOOR CLOSED', 'DOOR CLOSED'),
    ('STOPPED', 'STOPPED'),
]



class BaseModel(models.Model):
    # Represents an Base Model  which can be used as common fields in all other models (Abstract class)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class System(BaseModel):
    # Represents an System Model which is central controller of elevator
    name = models.CharField(max_length=200)


class Request(BaseModel):
    # Represents an request model for elevator access
    system = models.ForeignKey(System,on_delete=models.CASCADE,blank=True,null=True)
    floor = models.IntegerField()
    completed = models.BooleanField(default=False)


class Elevator(BaseModel):
    # Represents an elevator in the system
    system = models.ForeignKey(System,on_delete=models.CASCADE,related_name='system_elevators')
    request = models.ManyToManyField(Request,blank=True,related_name='request_elevators')
    floor = models.IntegerField(default=0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='IDLE')
    is_running = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=False)





