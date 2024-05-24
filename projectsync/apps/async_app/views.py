# Standard Library Imports
import os
import time
import threading

# Third-party Imports
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Local Imports
from async_app.models import Share, SharePriceUpdate, Task
from .serializers import ShareSerializer, SharePriceUpdateSerializer, TaskSerializer

from django.utils import timezone
from django.db import transaction


# API View to create shares data
class CreateSharesDataAPIView(APIView):
    def get(self, request):
        try:
            # Create 10,000 instances of Share model
            for i in range(1, 10000):
                Share.objects.create(
                    name=f'Share {i}',
                    price=i * 10,  # Example price calculation
                    created_at=timezone.now(),
                )
            return Response({'success': True, 'message': 'Shares created successfully'})
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        return Response({'success': False, 'message': 'Only GET requests are supported'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ViewSets for Share, Task, and SharePriceUpdate models
class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer


# ViewSets for Task model
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# ViewSets for SharePriceUpdate model
class SharePriceUpdateViewSet(viewsets.ModelViewSet):
    queryset = SharePriceUpdate.objects.all()
    serializer_class = SharePriceUpdateSerializer


# Function to update share prices in a background task
def update_share_prices_task(task_id):
    shares = Share.objects.all()
    
    with transaction.atomic():
        for share in shares:
            share.price += 1
            share.save()

            # Create SharePriceUpdate instance
            SharePriceUpdate.objects.create(
                share=share,
                price=share.price,
                old_price=share.price - 1,  # Assuming previous price was current price - 1
                task_id=task_id,
                updated_at=timezone.now()
            )


# API endpoint to initiate the task of updating share prices
@api_view(['POST'])
def update_share_prices(request):
    # Create a new task
    task = Task.objects.create(created_at=timezone.now())

    # Start a background thread to execute the task
    thread = threading.Thread(target=update_share_prices_task, args=(task.id,))
    thread.start()

    return Response({"task_id":task.id,"message": "Share price update task has been queued for processing. Check status later."},
                    status=status.HTTP_202_ACCEPTED)


# API endpoint to check the status of a task
@api_view(['GET'])
def task_status(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if task:
            count = SharePriceUpdate.objects.filter(task=task).count()
            all_shares = Share.objects.all().count()
            if count == all_shares:
                return Response({"status": "completed"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "in_progress"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No records"}, status=status.HTTP_404_NOT_FOUND)
    except Task.DoesNotExist:
        return Response({"error": "No records"}, status=status.HTTP_404_NOT_FOUND)
