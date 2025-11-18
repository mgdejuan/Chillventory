from datetime import date, timedelta
from django.utils import timezone
from sidebar.models import Notification

def check_inventory_and_notify(model, user, label, low_threshold=5, critical_threshold=2, expire_days=30):
    """
    For each item in model:
      - Create low / critical stock notifications if quantity <= thresholds
      - Create near-expiration notifications if expiration_date <= expire_days
    Avoid duplicates by checking existing unread notifications with same message.
    """
    today = date.today()
    soon = today + timedelta(days=expire_days)

    for item in model.objects.all():
        name = getattr(item, 'name', str(item))
        qty = getattr(item, 'quantity', None)

        # quantity alerts
        if qty is not None:
            if qty <= critical_threshold:
                msg = f"🔴 {label} '{name}' stock is CRITICAL ({qty} left)."
                if not Notification.objects.filter(user=user, message=msg, is_read=False).exists():
                    Notification.objects.create(user=user, message=msg)
            elif qty <= low_threshold:
                msg = f"🟠 {label} '{name}' stock is LOW ({qty} left)."
                if not Notification.objects.filter(user=user, message=msg, is_read=False).exists():
                    Notification.objects.create(user=user, message=msg)

        # expiration alerts (only if item has expiration_date attribute and it is set)
        if hasattr(item, 'expiration_date') and item.expiration_date:
            try:
                exp_date = item.expiration_date
                if today <= exp_date <= soon:
                    days_left = (exp_date - today).days
                    msg = f"⏳ {label} '{name}' will expire in {days_left} day{'s' if days_left != 1 else ''}."
                    if not Notification.objects.filter(user=user, message=msg, is_read=False).exists():
                        Notification.objects.create(user=user, message=msg)
            except Exception:
                # ignore malformed dates
                pass
