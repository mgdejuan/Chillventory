from sidebar.models import Notification

def notification_count(request):
<<<<<<< HEAD
    """Returns the number of unread notifications for the logged-in user."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        count = 0
    return {'notification_count': count}
=======
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
>>>>>>> 80c6c77791f8829d3528efd83f1827c0b1f090b1
