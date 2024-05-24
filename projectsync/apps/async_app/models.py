from django.db import models
from django.utils import timezone

#This MODEL will store every update time
class Task(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

# THIS MODEL will store all share 
class Share(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# This model will store every updates history corresponding to TASK and SHARE Model.
class SharePriceUpdate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_udpate")
    share = models.ForeignKey(Share, on_delete=models.CASCADE, related_name="price_updates")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(default=timezone.now)
