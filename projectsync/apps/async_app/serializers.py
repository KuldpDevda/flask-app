from rest_framework import serializers
from async_app.models import Share, Task, SharePriceUpdate

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SharePriceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePriceUpdate
        fields = '__all__'
