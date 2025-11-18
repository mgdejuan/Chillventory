from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
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
    Check all inventory and create notifications for low/critical stock or expired items.
    If 'user' is provided, only create notifications for that user.
    """
    items = []

    # Collect items to notify
    for f in Flavor.objects.all():
        if f.quantity <= getattr(f, 'critical_threshold', 2):
            items.append((f.name, "critical", "Flavor"))
        elif f.quantity <= getattr(f, 'low_threshold', 5):
            items.append((f.name, "low", "Flavor"))
        if f.expiration_date and f.expiration_date <= timezone.now().date():
            items.append((f.name, "expired", "Flavor"))

    for i in Ingredient.objects.all():
        if i.quantity <= getattr(i, 'critical_threshold', 2):
            items.append((i.name, "critical", "Ingredient"))
        elif i.quantity <= getattr(i, 'low_threshold', 5):
            items.append((i.name, "low", "Ingredient"))
        if i.expiration_date and i.expiration_date <= timezone.now().date():
            items.append((i.name, "expired", "Ingredient"))

    for t in Topping.objects.all():
        if t.quantity <= getattr(t, 'critical_threshold', 2):
            items.append((t.name, "critical", "Topping"))
        elif t.quantity <= getattr(t, 'low_threshold', 5):
            items.append((t.name, "low", "Topping"))
        if t.expiration_date and t.expiration_date <= timezone.now().date():
            items.append((t.name, "expired", "Topping"))

    for p in Packaging.objects.all():
        if p.quantity <= getattr(p, 'critical_threshold', 2):
            items.append((p.name, "critical", "Packaging"))
        elif p.quantity <= getattr(p, 'low_threshold', 5):
            items.append((p.name, "low", "Packaging"))

    users = [user] if user else list(User.objects.all())

    for u in users:
        for name, status, item_type in items:
            if status == "expired":
                message = f"{item_type} '{name}' has expired!"
            else:
                message = f"{item_type} '{name}' stock is {status}!"
            # Avoid duplicate notifications
            if not Notification.objects.filter(user=u, message=message, is_read=False).exists():
                Notification.objects.create(user=u, message=message, created_at=timezone.now())


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
    flavor.delete()
    update_stock_notifications(user=request.user)
    return redirect('flavors')


# ----------------- INGREDIENTS -----------------
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
<<<<<<< HEAD
            ingredient.name = request.POST.get('name')
            ingredient.price = request.POST.get('price')
            ingredient.quantity = int(request.POST.get('quantity') or 0)
            ingredient.expiration_date = request.POST.get('expiration_date') or None
            ingredient.save()
            Log.objects.create(user=request.user, action=f"updated ingredient '{ingredient.name}'", timestamp=timezone.now())
        else:
            name = request.POST.get('name')
            price = request.POST.get('price')
            quantity = int(request.POST.get('quantity') or 0)
            expiration_date = request.POST.get('expiration_date') or None
            Ingredient.objects.create(name=name, price=price, quantity=quantity, expiration_date=expiration_date)
            Log.objects.create(user=request.user, action=f"added ingredient '{name}'", timestamp=timezone.now())

        update_stock_notifications(user=request.user)
        return redirect('ingredients')

    ingredient_list = Ingredient.objects.all()
    return render(request, 'dashboard/ingredients.html', {'ingredients': ingredient_list, 'ingredient_to_edit': ingredient_to_edit})

=======

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
>>>>>>> a0c0bd2de432742220e28d3d3fe933f3016fbc27


def delete_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    Log.objects.create(user=request.user, action=f"deleted ingredient '{ingredient.name}'", timestamp=timezone.now())
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
