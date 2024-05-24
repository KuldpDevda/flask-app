from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Register the ShareViewSet, TaskViewSet, and SharePriceUpdateViewSet with the router.
router.register(r'shares', views.ShareViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'share-price-updates', views.SharePriceUpdateViewSet)

# Define the urlpatterns for our API
urlpatterns = [
    path('', include(router.urls)),
    path('home/', views.home, name='home'),
    path('create-shares/', views.CreateSharesDataAPIView.as_view(), name='create_shares'),
    path('update-share-prices/', views.update_share_prices, name='update_share_prices'),
    path('task-status/<int:task_id>/', views.task_status, name='task_status'),
]
