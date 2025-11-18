from django.utils import timezone
from datetime import timedelta
from dashboard.models import Flavor, Ingredient, Topping  # items with expiration
from sidebar.models import Notification


def notification_count(request):
    """Inject unread notification count + auto-generate new notifications."""
    if not request.user.is_authenticated:
        return {"notification_count": 0}

    # --------------------------
    # AUTO-GENERATE NOTIFICATIONS
    # --------------------------

    today = timezone.now().date()
    expiring_limit = today + timedelta(days=30)  # 30 days from now

    items = []

    # ---------- FLAVORS ----------
    for f in Flavor.objects.all():
        # Critical stock
        if f.quantity <= f.critical_threshold:
            items.append((f"{f.name} is CRITICAL in stock!", "critical"))

        # Low stock
        elif f.quantity <= f.low_threshold:
            items.append((f"{f.name} is LOW in stock!", "low"))

        # Expiration (if has expiration date)
        if f.expiration_date and today <= f.expiration_date <= expiring_limit:
            days_left = (f.expiration_date - today).days
            items.append((f"{f.name} will expire in {days_left} days!", "expiring"))

    # ---------- INGREDIENTS ----------
    for i in Ingredient.objects.all():
        if i.quantity <= 2:
            items.append((f"{i.name} is CRITICAL in stock!", "critical"))
        elif i.quantity <= 5:
            items.append((f"{i.name} is LOW in stock!", "low"))

        if i.expiration_date and today <= i.expiration_date <= expiring_limit:
            days_left = (i.expiration_date - today).days
            items.append((f"{i.name} will expire in {days_left} days!", "expiring"))

    # ---------- TOPPINGS ----------
    for t in Topping.objects.all():
        if t.quantity <= 2:
            items.append((f"{t.name} is CRITICAL in stock!", "critical"))
        elif t.quantity <= 5:
            items.append((f"{t.name} is LOW in stock!", "low"))

        if t.expiration_date and today <= t.expiration_date <= expiring_limit:
            days_left = (t.expiration_date - today).days
            items.append((f"{t.name} will expire in {days_left} days!", "expiring"))

    # ---------- CREATE NOTIFICATIONS ----------
    for message, tag in items:
        Notification.objects.get_or_create(
            user=request.user,
            message=message,
            defaults={"is_read": False}
        )

    # ---------- RETURN COUNT ----------
    unread = Notification.objects.filter(user=request.user, is_read=False).count()
    return {"notification_count": unread}
