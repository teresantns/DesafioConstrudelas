from .models import Referral
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

def delete_referrals_older_than_30_days():
    """
    This functions deletes all referral instances that are not accepted yet
    (status = False) and are older than 30 days
    """
    logger.info("Checking for expired referrals to delete.")
    referrals = Referral.objects.filter(status=False)
    for referral in referrals:
        tempo = timezone.now() - referral.created_at
        if tempo.days >= 30:
            referral.delete()
