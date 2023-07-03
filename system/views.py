from rest_framework.response import Response
from rest_framework import viewsets
from system.models import *
from system.serializers import *
from rest_framework import status
# Create your views here.


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

    def create(self, request, *args, **kwargs):
        serializer = ElevatorCreateSerializer(data=request.data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FloorRequestViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = FloorRequestSerializer(data=request.data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)