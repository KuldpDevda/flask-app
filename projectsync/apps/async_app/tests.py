import json
import concurrent.futures

from django.urls import reverse
from django.urls import reverse
from django.test import TestCase, Client
from django.test import TestCase, Client

from rest_framework import status
from rest_framework.test import APITestCase
from async_app.models import Share, Task, SharePriceUpdate
from async_app.serializers import ShareSerializer, TaskSerializer, SharePriceUpdateSerializer

class ShareViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('share-list')

    def test_list_shares(self):
        self.share1 = Share.objects.create(name='Share 1', price=100)
        self.share2 = Share.objects.create(name='Share 2', price=200)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_share(self):
        share = Share.objects.create(name='Test Share', price=150)
        url = reverse('share-detail', kwargs={'pk': share.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Share')

    def test_create_share(self):
        data = {'name': 'New Share', 'price': 300}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Share.objects.filter(name='New Share').exists())

    def test_delete_share(self):
        share = Share.objects.create(name='To Be Deleted', price=500)
        url = reverse('share-detail', kwargs={'pk': share.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Share.objects.filter(name='To Be Deleted').exists())

    # Add test cases for create, update, and delete operations

class TaskViewSetTestCase(APITestCase):
    def setUp(self):
        self.task1 = Task.objects.create()
        self.task2 = Task.objects.create()
        self.url = reverse('task-list')

    def test_list_tasks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task1.id)

    def test_create_task(self):
        data = {}  # Provide task data to create a new task
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(id=response.data['id']).exists())

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        data = {}  # Provide task data to update existing task
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        # Assert that task is updated with new data

    def test_partial_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        data = {}  # Provide partial task data to update existing task
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        # Assert that task is partially updated with new data

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())


class SharePriceUpdateViewSetTestCase(APITestCase):
    def setUp(self):
        self.task = Task.objects.create()  # Create a Task instance
        self.share = share = Share.objects.create(name='share1',price=100.00,)  # Set an initial price
        self.share_price_update1 = SharePriceUpdate.objects.create(task=self.task, share=self.share, price=150, old_price=100)
        self.share_price_update2 = SharePriceUpdate.objects.create(task=self.task, share=self.share, price=250, old_price=200)
        self.url = reverse('sharepriceupdate-list')

    def test_post_share_price_update(self):
        data = {'task': self.task.pk, 'share': self.share.pk, 'price': 300, 'old_price': 250}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SharePriceUpdate.objects.count(), 3)

    def test_get_share_price_updates(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_share_price_update(self):
        url = reverse('sharepriceupdate-detail', kwargs={'pk': self.share_price_update1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '150.00')

    def test_delete_share_price_update(self):
        url = reverse('sharepriceupdate-detail', kwargs={'pk': self.share_price_update1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SharePriceUpdate.objects.count(), 1)
    # Add test cases for list, retrieve, create, update, and delete operations


class TestSharePriceUpdate(TestCase):
    def setUp(self):
        self.client = Client()
    
    # This test case will test create share is working correctly or not
    def test_create_shares_data_api_view(self):
        response = self.client.get(reverse('create_shares'))  # Using the name defined in task/urls.py
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Share.objects.exists())
    
    # This test will test update share price is working correctly

    def test_update_share_prices(self):
        # Create a Share object
        share = Share.objects.create(
            name='share1',
            price=100,  
        )
        
        # Create a Task object
        task = Task.objects.create()
        
        # Send a POST request to update share prices
        response = self.client.post(reverse('update_share_prices'))
        
        # Check if the response status code is 202 (Accepted)
        self.assertEqual(response.status_code, 202)

    # This will test the task status response of the latest task or API hit
    def test_task_status(self):
        task = Task.objects.create()
        task_id = Task.objects.latest('id').id
        response = self.client.get(reverse('task_status', kwargs={'task_id': task_id}))
        self.assertEqual(response.status_code, 200)

        # Assuming shares update is not yet complete
        response_data = json.loads(response.content)
        self.assertIn('status', response_data)  # Check if 'status' key exists in the response data

        status = response_data['status']
        self.assertTrue(status in ['completed', 'in_progress'])  # Assert that status is either 'completed' or 'in_progress'

