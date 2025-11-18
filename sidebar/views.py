from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import Flavor, Ingredient, Topping, Packaging
from .models import Notification, LogHistory

# ----------------- HELPER FUNCTION -----------------
def update_stock_notifications(item, user=None):
    """
    Updates stock notifications for a single item.
    Removes notifications if stock is now above low threshold.
    """
    critical_threshold = getattr(item, 'critical_threshold', 2)
    low_threshold = getattr(item, 'low_threshold', 5)

    if user is None:
        users = User.objects.all()
    else:
        users = [user]

    for u in users:
        # Delete notifications for this item that are no longer relevant
        Notification.objects.filter(user=u, message__icontains=item.name, is_read=False).delete()

        # Only create notification if stock is low or critical
        if item.quantity <= critical_threshold:
            Notification.objects.create(
                user=u,
                message=f"Critical stock: {item.__class__.__name__} '{item.name}' is very low ({item.quantity})",
                is_read=False
            )
        elif item.quantity <= low_threshold:
            Notification.objects.create(
                user=u,
                message=f"Low stock: {item.__class__.__name__} '{item.name}' is running low ({item.quantity})",
                is_read=False
            )


def log_action(user, action, item):
    """
    Creates a LogHistory entry for an action on an item
    """
    LogHistory.objects.create(
        user=user,
        action_taken=action,
        product_name=item.name,
        stock_status=f"Quantity: {item.quantity}"
    )

# ----------------- INVENTORY VIEW -----------------
@login_required
def inventory(request):
    stock = {
        'flavors': Flavor.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'toppings': Topping.objects.all(),
        'packaging': Packaging.objects.all(),
    }
    return render(request, 'sidebar/inventory.html', {'stock': stock})

# ----------------- EDIT VIEWS -----------------
@login_required
def edit_item(request, model_class, item_id):
    item = get_object_or_404(model_class, id=item_id)
    if request.method == 'POST':
        item.quantity = int(request.POST.get('quantity') or 0)
        item.save()

        # Log and update notifications
        log_action(request.user, 'UPDATE', item)
        update_stock_notifications(item, user=request.user)

        return redirect('inventory')

    return render(request, 'sidebar/edit_item.html', {'item': item})

# Wrapper views for each type
@login_required
def edit_flavor(request, flavor_id):
    return edit_item(request, Flavor, flavor_id)

@login_required
def edit_ingredient(request, ingredient_id):
    return edit_item(request, Ingredient, ingredient_id)

@login_required
def edit_topping(request, topping_id):
    return edit_item(request, Topping, topping_id)

@login_required
def edit_packaging(request, packaging_id):
    return edit_item(request, Packaging, packaging_id)

# ----------------- RESTOCK VIEWS -----------------
@login_required
def restock_item(request, model_class, item_id, amount=10):
    item = get_object_or_404(model_class, id=item_id)
    update_stock_notifications(item, restock_amount=amount, user=request.user)
    log_action(request.user, 'UPDATE', item)
    return redirect('inventory')

# Wrapper views for each type
@login_required
def restock_flavor(request, flavor_id):
    return restock_item(request, Flavor, flavor_id)

@login_required
def restock_ingredient(request, ingredient_id):
    return restock_item(request, Ingredient, ingredient_id)

@login_required
def restock_topping(request, topping_id):
    return restock_item(request, Topping, topping_id)

@login_required
def restock_packaging(request, packaging_id):
    return restock_item(request, Packaging, packaging_id)

# ----------------- NOTIFICATIONS -----------------
def notifications(request):
    # Only show unread notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    return render(request, 'sidebar/notifications.html', {'notifications': notifications})

@login_required
def notifications_list(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'sidebar/notifications.html', {'notifications': notes})

@login_required
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return redirect('notifications')

# ----------------- LOG HISTORY -----------------
@login_required
def log_history(request):
    logs = LogHistory.objects.all().order_by('-date_and_time')
    return render(request, 'dashboard/log_history.html', {'logs': logs})

# ----------------- HOME PAGE -----------------
@login_required
def home(request):
    recent_logs = LogHistory.objects.all().order_by('-date_and_time')[:10]
    return render(request, 'sidebar/home.html', {'recent_logs': recent_logs})

# ----------------- STATIC PAGES -----------------
@login_required
def about(request):
    return render(request, 'sidebar/about.html')

@login_required
def logout_view(request):
    return render(request, 'sidebar/logout_view.html')
