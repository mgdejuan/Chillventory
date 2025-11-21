from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import Flavor, Ingredient, Topping, Packaging
from .models import Notification, LogHistory

# ----------------- HELPER FUNCTION -----------------
def update_stock_notifications(item, restock_amount=0):
    """
    Updates item quantity if restock_amount > 0, then updates notifications for all users.
    Safe for all item types (Flavor, Ingredient, Topping, Packaging).
    """
<<<<<<< HEAD
    # Restock if needed
    if restock_amount > 0:
        item.quantity += restock_amount
        item.save()

    # Clear existing unread notifications for this item
    Notification.objects.filter(message__icontains=item.name, is_read=False).delete()

    # Set thresholds safely
    critical_threshold = getattr(item, 'critical_threshold', 2)
    low_threshold = getattr(item, 'low_threshold', 5)
=======
    critical_threshold = getattr(item, 'critical_threshold', 5)
    low_threshold = getattr(item, 'low_threshold', 10)
>>>>>>> 80c6c77791f8829d3528efd83f1827c0b1f090b1

    # Recreate notifications for all users if stock is low
    for user in User.objects.all():
        if item.quantity <= critical_threshold:
            message = f"Critical stock: {item.__class__.__name__} '{item.name}' is very low ({item.quantity})"
            Notification.objects.create(user=user, message=message)
        elif item.quantity <= low_threshold:
            message = f"Low stock: {item.__class__.__name__} '{item.name}' is running low ({item.quantity})"
            Notification.objects.create(user=user, message=message)


# ----------------- RESTOCK VIEWS -----------------
@login_required
def restock_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    update_stock_notifications(flavor, restock_amount=10)
    return redirect('inventory')


@login_required
def restock_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    update_stock_notifications(ingredient, restock_amount=10)
    return redirect('inventory')


@login_required
def restock_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    update_stock_notifications(topping, restock_amount=10)
    return redirect('inventory')


@login_required
def restock_packaging(request, id):
    packaging = get_object_or_404(Packaging, id=id)
    update_stock_notifications(packaging, restock_amount=10)
    return redirect('inventory')


# ----------------- HOME PAGE -----------------
@login_required
def home(request):
    recent_logs = LogHistory.objects.all().order_by('-date_and_time')[:10]
    return render(request, 'sidebar/home.html', {'recent_logs': recent_logs})


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

# ----------------- UPDATE VIEWS -----------------

@login_required
def edit_flavor(request, flavor_id):
    flavor = get_object_or_404(Flavor, id=flavor_id)
    if request.method == 'POST':
        flavor.quantity = request.POST.get('quantity')
        flavor.save()
        return redirect('inventory')
    return render(request, 'flavor.html', {'item': flavor})

@login_required
def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        ingredient.quantity = request.POST.get('quantity')
        ingredient.save()
        return redirect('inventory')
    return render(request, 'ingredient.html', {'item': ingredient})

@login_required
def edit_topping(request, topping_id):
    topping = get_object_or_404(Topping, id=topping_id)
    if request.method == 'POST':
        topping.quantity = request.POST.get('quantity')
        topping.save()
        return redirect('inventory')
    return render(request, 'topping.html', {'item': topping})

@login_required
def edit_packaging(request, packaging_id):
    packaging = get_object_or_404(Packaging, id=packaging_id)
    if request.method == 'POST':
        packaging.quantity = request.POST.get('quantity')
        packaging.save()
        return redirect('inventory')
    return render(request, 'packaging.html', {'item': packaging})

# ----------------- NOTIFICATIONS -----------------
@login_required
def notifications(request):
    # Generate notifications dynamically for all items (without restocking)
    for item in list(Flavor.objects.all()) + list(Ingredient.objects.all()) + list(Topping.objects.all()) + list(Packaging.objects.all()):
        update_stock_notifications(item)

    notifications = Notification.objects.filter(is_read=False, user=request.user).order_by('-created_at')
    return render(request, 'sidebar/notifications.html', {'notifications': notifications})

<<<<<<< HEAD

# ----------------- LOG HISTORY PAGE -----------------
=======
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

def clear_all_notifications(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications')

# ----------------- LOG HISTORY -----------------
>>>>>>> 80c6c77791f8829d3528efd83f1827c0b1f090b1
@login_required
def log_history(request):
    return render(request, 'dashboard/log_history.html')


# ----------------- ABOUT PAGE -----------------
@login_required
def about(request):
    return render(request, 'sidebar/about.html')


# ----------------- LOGOUT PAGE -----------------
@login_required
def logout_view(request):
    return render(request, 'logout_view.html')
