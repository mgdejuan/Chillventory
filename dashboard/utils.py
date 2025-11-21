from django.utils import timezone
from django.contrib.auth.models import User
from .models import Flavor, Ingredient, Topping, Packaging, Notification

def update_stock_and_expiration_notifications(user=None):
    """
    Updates stock and expiration notifications for all items.
    - Critical stock: 5 or below
    - Low stock: 6–10
    - Expiring soon: within 5 days
    - Notifications disappear if resolved (quantity > 10 or expiration passed)
    """
    critical_threshold = 5
    low_threshold_min = 6
    low_threshold_max = 10
    expire_days = 5  # warn if expiration is within 5 days

    if user is None:
        users = User.objects.all()
    else:
        users = [user]

    now = timezone.now().date()

    all_items = [
        (Flavor.objects.all(), "Flavor"),
        (Ingredient.objects.all(), "Ingredient"),
        (Topping.objects.all(), "Topping"),
        (Packaging.objects.all(), "Packaging"),
    ]

    for items, item_type in all_items:
        for item in items:
            for u in users:
                # Remove old notifications for this item first
                Notification.objects.filter(user=u, message__icontains=item.name, is_read=False).delete()

                # 1️⃣ Stock notifications
                if hasattr(item, "quantity"):
                    if item.quantity <= critical_threshold:
                        Notification.objects.create(
                            user=u,
                            message=f"🔴 {item_type} '{item.name}' stock is CRITICAL ({item.quantity} left).",
                            is_read=False
                        )
                    elif low_threshold_min <= item.quantity <= low_threshold_max:
                        Notification.objects.create(
                            user=u,
                            message=f"🟠 {item_type} '{item.name}' stock is LOW ({item.quantity} left).",
                            is_read=False
                        )

                # 2️⃣ Expiration notifications (if item has expiration_date)
                expiration_date = getattr(item, "expiration_date", None)
                if expiration_date:
                    days_left = (expiration_date - now).days
                    if days_left < 0:
                        Notification.objects.create(
                            user=u,
                            message=f"❌ {item_type} '{item.name}' has EXPIRED!",
                            is_read=False
                        )
                    elif days_left <= expire_days:
                        Notification.objects.create(
                            user=u,
                            message=f"⏳ {item_type} '{item.name}' will expire in {days_left} days.",
                            is_read=False
                        )


