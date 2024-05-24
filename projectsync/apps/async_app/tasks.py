from celery import shared_task
from async_app.models import Share, SharePriceUpdate
from django.db import transaction
from django.utils import timezone

import logging


logger = logging.getLogger(__name__)

"""
THIS task is executing in aync by using .delay() and we are running this task through celery
In this we are updating all shares by 1 by taking foreign key of task(time of api hitting) and track all 
updates in SharePriceUpdate model
"""

@shared_task
def update_share_prices_task(task_id):
    # Get all shares
    logger.info("Task started. Task ID: %s", task_id)
    shares = Share.objects.all()

    # Update share prices within a transaction
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