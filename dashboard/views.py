from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Flavor, Ingredient, Topping, Packaging, Log
from sidebar.models import Notification

# ----------------- DASHBOARD -----------------
@login_required
def dashboard(request):
    recent_logs = Log.objects.all().order_by('-timestamp')[:10]
    return render(request, 'dashboard/home.html', {'recent_logs': recent_logs})


# ----------------- REAL-TIME NOTIFICATIONS HELPER -----------------
def update_stock_notifications(user=None):
    """
    Check inventory and create notifications for:
    - Critical stock: 5 or below
    - Low stock: 6–10
    - Expired items
    - Expiring soon items (within 30 days)
    Remove notifications if resolved (stock above 10, not expired)
    """
    today = timezone.now().date()
    expiring_soon_limit = today + timedelta(days=30)

    items_to_notify = []
    items_resolved = []

    # Helper to check stock and expiration
    def check_item(obj, item_type):
        is_critical = obj.quantity <= 5
        is_low = 6 <= obj.quantity <= 10
        is_expired = obj.expiration_date and obj.expiration_date <= today
        is_expiring_soon = obj.expiration_date and today < obj.expiration_date <= expiring_soon_limit

        # Stock notifications
        if is_critical:
            items_to_notify.append((obj.name, "critical", item_type))
        elif is_low:
            items_to_notify.append((obj.name, "low", item_type))
        else:
            items_resolved.append((obj.name, item_type, ["critical", "low"]))

        # Expiration notifications
        if is_expired:
            items_to_notify.append((obj.name, "expired", item_type))
        elif is_expiring_soon:
            days_left = (obj.expiration_date - today).days
            items_to_notify.append((obj.name, "expiring_soon", item_type, days_left))

    # Check all items
    for f in Flavor.objects.all():
        check_item(f, "Flavor")

    for i in Ingredient.objects.all():
        check_item(i, "Ingredient")

    for t in Topping.objects.all():
        check_item(t, "Topping")

    # Packaging has no expiration
    for p in Packaging.objects.all():
        if p.quantity <= 5:
            items_to_notify.append((p.name, "critical", "Packaging"))
        elif 6 <= p.quantity <= 10:
            items_to_notify.append((p.name, "low", "Packaging"))
        else:
            items_resolved.append((p.name, "Packaging", ["critical", "low"]))

    # Determine users to notify
    users = [user] if user else list(User.objects.all())

    # Create/update notifications
    for u in users:
        for item in items_to_notify:
            # Unpack depending on type
            if len(item) == 4:  # expiring soon
                name, status, item_type, days_left = item
            else:
                name, status, item_type = item
                days_left = None

            if status == "expired":
                message = f"❌ {item_type} '{name}' has expired!"
            elif status == "expiring_soon":
                message = f"⚠️ {item_type} '{name}' will expire in {days_left} days!"
            elif status == "critical":
                message = f"🔴 {item_type} '{name}' stock is CRITICAL!"
            else:  # low
                message = f"🟠 {item_type} '{name}' stock is LOW!"

            # Avoid duplicate unread notifications
            if not Notification.objects.filter(user=u, message=message, is_read=False).exists():
                Notification.objects.create(user=u, message=message, created_at=timezone.now())

    # Delete notifications for resolved stock issues
    for u in users:
        for name, item_type, statuses in items_resolved:
            for status in statuses:
                if status == "critical":
                    message = f"🔴 {item_type} '{name}' stock is CRITICAL!"
                elif status == "low":
                    message = f"🟠 {item_type} '{name}' stock is LOW!"
                Notification.objects.filter(user=u, message=message, is_read=False).delete()


# ----------------- FLAVORS -----------------
def flavors(request):
    edit_id = request.GET.get('edit')
    flavor_to_edit = get_object_or_404(Flavor, id=edit_id) if edit_id else None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_flavor':
            flavor_id = request.POST.get('flavor_id')
            flavor = get_object_or_404(Flavor, id=flavor_id)
            flavor.name = request.POST.get('name')
            flavor.price = request.POST.get('price')
            flavor.quantity = int(request.POST.get('quantity') or 0)
            flavor.expiration_date = request.POST.get('expiration_date') or None
            flavor.save()
            Log.objects.create(user=request.user, action=f"updated flavor '{flavor.name}'", timestamp=timezone.now())
        else:
            name = request.POST.get('name')
            price = request.POST.get('price')
            quantity = int(request.POST.get('quantity') or 0)
            expiration_date = request.POST.get('expiration_date') or None
            Flavor.objects.create(name=name, price=price, quantity=quantity, expiration_date=expiration_date)
            Log.objects.create(user=request.user, action=f"added flavor '{name}'", timestamp=timezone.now())

        # Update notifications after any change
        update_stock_notifications(user=request.user)
        return redirect('flavors')

    flavors_list = Flavor.objects.all()
    return render(request, 'dashboard/flavors.html', {'flavors': flavors_list, 'flavor_to_edit': flavor_to_edit})


def delete_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    Log.objects.create(user=request.user, action=f"deleted flavor '{flavor.name}'", timestamp=timezone.now())
    Notification.objects.filter(message__icontains=flavor.name).delete()
    flavor.delete()
    update_stock_notifications(user=request.user)
    return redirect('flavors')

# ----------------- INGREDIENTS -----------------
def ingredients(request):
    edit_id = request.GET.get('edit')
    ingredient_to_edit = get_object_or_404(Ingredient, id=edit_id) if edit_id else None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_ingredient":
            # UPDATE EXISTING INGREDIENT
            ingredient_id = request.POST.get("ingredient_id")
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            ingredient.name = request.POST.get("name")
            ingredient.price = request.POST.get("price") or 0
            ingredient.quantity = int(request.POST.get("quantity") or 0)
            ingredient.expiration_date = request.POST.get("expiration_date") or None
            ingredient.save()

            Log.objects.create(
                user=request.user,
                action=f"updated ingredient '{ingredient.name}'",
                timestamp=timezone.now()
            )

        else:
            # ADD NEW INGREDIENT
            name = request.POST.get("name")
            price = request.POST.get("price") or 0
            quantity = int(request.POST.get("quantity") or 0)
            expiration_date = request.POST.get("expiration_date") or None

            Ingredient.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

            Log.objects.create(
                user=request.user,
                action=f"added ingredient '{name}'",
                timestamp=timezone.now()
            )

        return redirect("ingredients")

    # GET — display page
    ingredients_list = Ingredient.objects.all()
    return render(request, "dashboard/ingredients.html", {
        "ingredients": ingredients_list,
        "ingredient_to_edit": ingredient_to_edit,
    })


def delete_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    Log.objects.create(user=request.user, action=f"deleted ingredient '{ingredient.name}'", timestamp=timezone.now())
    Notification.objects.filter(message__icontains=ingredient.name).delete()
    ingredient.delete()
    update_stock_notifications(user=request.user)
    return redirect('ingredients')


# ----------------- TOPPINGS -----------------
def toppings(request):
    edit_id = request.GET.get('edit')
    topping_to_edit = get_object_or_404(Topping, id=edit_id) if edit_id else None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_topping':
            topping_id = request.POST.get('topping_id')
            topping = get_object_or_404(Topping, id=topping_id)
            topping.name = request.POST.get('name')
            topping.price = request.POST.get('price')
            topping.quantity = int(request.POST.get('quantity') or 0)
            topping.expiration_date = request.POST.get('expiration_date') or None
            topping.save()
            Log.objects.create(user=request.user, action=f"updated topping '{topping.name}'", timestamp=timezone.now())
        else:
            name = request.POST.get('name')
            price = request.POST.get('price')
            quantity = int(request.POST.get('quantity') or 0)
            expiration_date = request.POST.get('expiration_date') or None
            Topping.objects.create(name=name, price=price, quantity=quantity, expiration_date=expiration_date)
            Log.objects.create(user=request.user, action=f"added topping '{name}'", timestamp=timezone.now())

        update_stock_notifications(user=request.user)
        return redirect('toppings')

    topping_list = Topping.objects.all()
    return render(request, 'dashboard/toppings.html', {'toppings': topping_list, 'topping_to_edit': topping_to_edit})


def delete_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    Log.objects.create(user=request.user, action=f"deleted topping '{topping.name}'", timestamp=timezone.now())
    Notification.objects.filter(message__icontains=topping.name).delete()
    topping.delete()
    update_stock_notifications(user=request.user)
    return redirect('toppings')


# ----------------- PACKAGING -----------------
def packaging(request):
    edit_id = request.GET.get('edit')
    packaging_to_edit = get_object_or_404(Packaging, id=edit_id) if edit_id else None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_packaging':
            packaging_id = request.POST.get('packaging_id')
            pkg = get_object_or_404(Packaging, id=packaging_id)
            pkg.name = request.POST.get('name')
            pkg.price = request.POST.get('price')
            pkg.quantity = int(request.POST.get('quantity') or 0)
            pkg.save()
            Log.objects.create(user=request.user, action=f"updated packaging '{pkg.name}'", timestamp=timezone.now())
        else:
            name = request.POST.get('name')
            price = request.POST.get('price')
            quantity = int(request.POST.get('quantity') or 0)
            Packaging.objects.create(name=name, price=price, quantity=quantity)
            Log.objects.create(user=request.user, action=f"added packaging '{name}'", timestamp=timezone.now())

        update_stock_notifications(user=request.user)
        return redirect('packaging')

    packaging_list = Packaging.objects.all()
    return render(request, 'dashboard/packaging.html', {'packagings': packaging_list, 'packaging_to_edit': packaging_to_edit})


def delete_packaging(request, id):
    pkg = get_object_or_404(Packaging, id=id)
    Log.objects.create(user=request.user, action=f"deleted packaging '{pkg.name}'", timestamp=timezone.now())
    Notification.objects.filter(message__icontains=pkg.name).delete()
    pkg.delete()
    update_stock_notifications(user=request.user)
    return redirect('packaging')


# ----------------- INVENTORY -----------------
@login_required
def inventory(request):
    stock = {
        'flavors': Flavor.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'toppings': Topping.objects.all(),
        'packaging': Packaging.objects.all(),
    }
    return render(request, 'dashboard/inventory.html', {'stock': stock})


# ----------------- RESTOCK -----------------
@login_required
def restock_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    flavor.quantity += 10
    flavor.save()
    update_stock_notifications(user=request.user)
    return redirect('inventory')


@login_required
def restock_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    ingredient.quantity += 10
    ingredient.save()
    update_stock_notifications(user=request.user)
    return redirect('inventory')


@login_required
def restock_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    topping.quantity += 10
    topping.save()
    update_stock_notifications(user=request.user)
    return redirect('inventory')


@login_required
def restock_packaging(request, id):
    pack = get_object_or_404(Packaging, id=id)
    pack.quantity += 10
    pack.save()
    update_stock_notifications(user=request.user)
    return redirect('inventory')


# ----------------- LOG HISTORY -----------------
@login_required
def log_history(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/log_history.html', {'logs': logs})
