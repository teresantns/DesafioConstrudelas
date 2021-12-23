from datetime import timedelta
from .models import Referral
from django.utils import timezone


def delete_referrals_older_than_30_days():
    """
    This functions deletes all referral instances that are not accepted yet
    (status = False) and are older than 30 days
    """
    referrals = Referral.objects.filter(status=False)
    for referral in referrals:
        tempo = timezone.now() - referral.created_at
        if tempo.days > 30:
            referral.delete()
