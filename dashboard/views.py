from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Flavor, Ingredient, Topping, Packaging, Log
from sidebar.models import Notification  # Make sure Notification model is imported

# ----------------- DASHBOARD -----------------
def dashboard(request):
    return render(request, 'dashboard/home.html')

# ----------------- FLAVORS -----------------
def flavors(request):
    # Detect edit mode
    edit_id = request.GET.get('edit')
    flavor_to_edit = get_object_or_404(Flavor, id=edit_id) if edit_id else None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_flavor':
            # EDIT EXISTING FLAVOR
            flavor_id = request.POST.get('flavor_id')
            flavor = get_object_or_404(Flavor, id=flavor_id)

            flavor.name = request.POST.get('name')
            flavor.price = request.POST.get('price')
            flavor.quantity = int(request.POST.get('quantity') or 0)
            flavor.expiration_date = request.POST.get('expiration_date') or None
            flavor.save()

            Log.objects.create(
                user=request.user,
                action=f"updated flavor '{flavor.name}'",
                timestamp=timezone.now()
            )
        else:
            # ADD NEW FLAVOR
            name = request.POST.get('name')
            price = request.POST.get('price')
            quantity = int(request.POST.get('quantity') or 0)
            expiration_date = request.POST.get('expiration_date') or None

            Flavor.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

            Log.objects.create(
                user=request.user,
                action=f"added flavor '{name}'",
                timestamp=timezone.now()
            )

        return redirect('flavors')

    # GET request: show all flavors
    flavors_list = Flavor.objects.all()
    return render(request, 'dashboard/flavors.html', {
        'flavors': flavors_list,
        'flavor_to_edit': flavor_to_edit
    })

def delete_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    Log.objects.create(
        user=request.user,
        action=f"deleted flavor '{flavor.name}'",
        timestamp=timezone.now()
    )
    flavor.delete()
    return redirect('flavors')


# ----------------- INGREDIENTS -----------------
def ingredients(request):
    edit_id = request.GET.get('edit')
    ingredient_to_edit = None

    if edit_id:
        try:
            ingredient_to_edit = Ingredient.objects.get(id=edit_id)
        except Ingredient.DoesNotExist:
            ingredient_to_edit = None

    if request.method == 'POST':
        action = request.POST.get('action')

        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity') or 0)
        expiration_date = request.POST.get('expiration_date') or None

        if action == 'update_ingredient':
            # UPDATE mode
            ingredient_id = request.POST.get('ingredient_id')
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)

            ingredient.name = name
            ingredient.price = price
            ingredient.quantity = quantity
            ingredient.expiration_date = expiration_date
            ingredient.save()

            Log.objects.create(
                user=request.user,
                action=f"updated ingredient '{ingredient.name}'",
                timestamp=timezone.now()
            )

        else:
            # ADD mode
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

        return redirect('ingredients')

    # GET request
    ingredients_list = Ingredient.objects.all()
    return render(request, 'dashboard/ingredients.html', {
        'ingredients': ingredients_list,
        'ingredient_to_edit': ingredient_to_edit
    })

def delete_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    Log.objects.create(
        user=request.user,
        action=f"deleted ingredient '{ingredient.name}'",
        timestamp=timezone.now()
    )
    ingredient.delete()
    return redirect('ingredients')


# ----------------- TOPPINGS -----------------
def toppings(request):
    edit_id = request.GET.get('edit')
    topping_to_edit = get_object_or_404(Topping, id=edit_id) if edit_id else None

    if request.method == "POST":
        action = request.POST.get('action')

        # ---------- UPDATE TOPPING ----------
        if action == 'update_topping':
            topping_id = request.POST.get('topping_id')
            topping = get_object_or_404(Topping, id=topping_id)

            topping.name = request.POST.get('name') or topping.name
            topping.price = request.POST.get('price') or topping.price
            topping.quantity = int(request.POST.get('quantity') or 0)
            topping.expiration_date = request.POST.get('expiration_date') or None
            topping.save()

            Log.objects.create(
                user=request.user,
                action=f"updated topping '{topping.name}'",
                timestamp=timezone.now()
            )

        # ---------- CREATE TOPPING ----------
        else:
            name = request.POST.get('name') or None
            price = request.POST.get('price') or 0
            quantity = int(request.POST.get('quantity') or 0)
            expiration_date = request.POST.get('expiration_date') or None

            Topping.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

            Log.objects.create(
                user=request.user,
                action=f"added topping '{name}'",
                timestamp=timezone.now()
            )

        return redirect('toppings')

    # ---------- DISPLAY PAGE ----------
    toppings_list = Topping.objects.all()
    return render(request, 'dashboard/toppings.html', {
        'toppings': toppings_list,
        'topping_to_edit': topping_to_edit
    })


# ---------- DELETE TOPPING ----------
def delete_topping(request, id):
    topping = get_object_or_404(Topping, id=id)

    Log.objects.create(
        user=request.user,
        action=f"deleted topping '{topping.name}'",
        timestamp=timezone.now()
    )

    topping.delete()
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
def update_stock_notifications():
    """Check all inventory and create notifications for low/critical stock"""
    items = []

    for f in Flavor.objects.all():
        if f.quantity <= f.critical_threshold:
            items.append((f.name, "critical"))
        elif f.quantity <= f.low_threshold:
            items.append((f.name, "low"))

    for i in Ingredient.objects.all():
        if i.quantity <= 2:
            items.append((i.name, "critical"))
        elif i.quantity <= 5:
            items.append((i.name, "low"))

    for t in Topping.objects.all():
        if t.quantity <= 2:
            items.append((t.name, "critical"))
        elif t.quantity <= 5:
            items.append((t.name, "low"))

    for p in Packaging.objects.all():
        if p.quantity <= 2:
            items.append((p.name, "critical"))
        elif p.quantity <= 5:
            items.append((p.name, "low"))

    for name, status in items:
        message = f"{name} stock is {status}!"
        if not Notification.objects.filter(message=message, is_read=False).exists():
            Notification.objects.create(message=message, created_at=timezone.now())


@login_required
def restock_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    flavor.quantity += 10
    flavor.save()
    update_stock_notifications()
    return redirect('inventory')


@login_required
def restock_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    ingredient.quantity += 10
    ingredient.save()
    update_stock_notifications()
    return redirect('inventory')


@login_required
def restock_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    topping.quantity += 10
    topping.save()
    update_stock_notifications()
    return redirect('inventory')


@login_required
def restock_packaging(request, id):
    pack = get_object_or_404(Packaging, id=id)
    pack.quantity += 10
    pack.save()
    update_stock_notifications()
    return redirect('inventory')


# ----------------- LOG HISTORY -----------------
@login_required
def log_history(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/log_history.html', {'logs': logs})
