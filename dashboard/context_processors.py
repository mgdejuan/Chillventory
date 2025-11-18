from sidebar.models import Notification

def notification_count(request):
    """Return unread notification count only (no expiration checks)."""
    if not request.user.is_authenticated:
        return {
            "notification_count": 0,
            "notifications": []
        }

    # Get unread notifications only
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return {
        "notification_count": notifications.count(),
        "notifications": notifications
    }
