from rest_framework.response import Response
from rest_framework import viewsets
from system.models import *
from system.serializers import *
from rest_framework import status
from django.db import transaction
from django.db.models import Min, F,Func
# Create your views here.


@transaction.atomic
def assign_elevator(system):
    first_object = Request.objects.filter(system=system,completed=False).order_by('created_at').first()
    if first_object:
        floor = first_object.floor
        closest_object = Elevator.objects.filter(
            system=system,
            status="IDLE",
            is_running=True
        ).annotate(diff=Func(F('floor') - floor, function='ABS')).order_by('diff').first()
        print(closest_object)
        if closest_object:
            closest_object.request.add(first_object)
            current_floor = closest_object.floor
            if current_floor == floor:
                closest_object.status = "DOOR OPEN"
            if current_floor > floor:
                closest_object.status = "MOVING DOWN"
            if current_floor < floor:
                closest_object.status = "MOVING UP"
            first_object.completed = True
            first_object.save()
            closest_object.save()


class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    def retrieve(self, request, *args, **kwargs):
        next = request.query_params.get('next')
        obj = self.get_object()
        if next:
            if obj.status == "MOVING UP":
                return Response({"nextDestination":obj.floor + 1,"status":obj.status})
            elif obj.status == "MOVING DOWN":
                return Response({"nextDestination":obj.floor - 1,"status":obj.status})
            else:
                return Response({"nextDestination": obj.floor , "status": obj.status})
        else:
            serializer = self.get_serializer(obj)
            return Response(serializer.data,status=status.HTTP_200_OK)
    def list(self, request, *args, **kwargs):
        stat = request.query_params.get('status')
        system = request.query_params.get('system')

        if system:
            if stat in ['IDLE','MOVING UP','MOVING DOWN','DOOR OPEN','DOOR CLOSED','STOPPED']:
                objs = Elevator.objects.filter(status=stat,system=system)
                serializer = self.get_serializer(objs,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = ElevatorCreateSerializer(data=request.data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()
        data['elevator'] = instance.id
        serializer = ElevatorSerializer(instance,data=request.data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            if serializer.data['status'] == "IDLE":
                assign_elevator(instance.system.id)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FloorRequestViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = FloorRequestSerializer(data=request.data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            system = serializer.data['system']
            assign_elevator(system)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)