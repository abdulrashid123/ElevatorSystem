from rest_framework import serializers
from system.models import *

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'


class ElevatorCreateSerializer(serializers.Serializer):
    system = serializers.PrimaryKeyRelatedField(queryset=System.objects.all())
    floors = serializers.IntegerField()

    def create(self, validated_data):
        system = validated_data['system']
        for floor in range(validated_data['floors']):
            Elevator.objects.create(
                system=system
            )
        return system


class FloorRequestSerializer(serializers.Serializer):
    system = serializers.PrimaryKeyRelatedField(queryset=System.objects.all())
    floor = serializers.IntegerField()

    def create(self, validated_data):
        system = validated_data['system']
        floor = validated_data['floor']
        obj = Request.objects.create(
            system=system,
            floor=floor
        )
        return obj