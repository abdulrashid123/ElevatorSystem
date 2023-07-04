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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class System(BaseModel):
    name = models.CharField(max_length=200)


class Request(BaseModel):
    system = models.ForeignKey(System,on_delete=models.CASCADE,blank=True,null=True)
    floor = models.IntegerField()
    completed = models.BooleanField(default=False)


class Elevator(BaseModel):
    system = models.ForeignKey(System,on_delete=models.CASCADE)
    request = models.ManyToManyField(Request,blank=True,related_name='request_elevators')
    floor = models.IntegerField(default=0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='IDLE')
    is_running = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=False)





