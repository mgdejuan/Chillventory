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
    edit_id = request.GET.get('edit')
    flavor_to_edit = get_object_or_404(Flavor, id=edit_id) if edit_id else None

    if request.method == 'POST':
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

    flavors_list = Flavor.objects.all()
    return render(request, 'dashboard/flavors.html', {
        'flavors': flavors_list,
        'flavor_to_edit': flavor_to_edit
    })

def delete_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    flavor.delete()
    return redirect('flavors')


# ----------------- INGREDIENTS -----------------
def ingredients(request):
    edit_id = request.GET.get('edit')
    ingredient_to_edit = get_object_or_404(Ingredient, id=edit_id) if edit_id else None

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity') or 0)
        expiration_date = request.POST.get('expiration_date') or None

        if ingredient_to_edit:
            ingredient_to_edit.name = name
            ingredient_to_edit.price = price
            ingredient_to_edit.quantity = quantity
            ingredient_to_edit.expiration_date = expiration_date
            ingredient_to_edit.save()
        else:
            Ingredient.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )
        return redirect('ingredients')

    ingredients_list = Ingredient.objects.all()
    return render(request, 'dashboard/ingredients.html', {
        'ingredients': ingredients_list,
        'ingredient_to_edit': ingredient_to_edit
    })

def delete_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    ingredient.delete()
    return redirect('ingredients')


# ----------------- TOPPINGS -----------------
def toppings(request):
    edit_id = request.GET.get('edit')
    topping_to_edit = get_object_or_404(Topping, id=edit_id) if edit_id else None

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity') or 0)
        expiration_date = request.POST.get('expiration_date') or None

        if topping_to_edit:
            topping_to_edit.name = name
            topping_to_edit.price = price
            topping_to_edit.quantity = quantity
            topping_to_edit.expiration_date = expiration_date
            topping_to_edit.save()
        else:
            Topping.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )
        return redirect('toppings')

    toppings_list = Topping.objects.all()
    return render(request, 'dashboard/toppings.html', {
        'toppings': toppings_list,
        'topping_to_edit': topping_to_edit
    })

def delete_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    topping.delete()
    return redirect('toppings')


# ----------------- PACKAGING -----------------
def add_packaging(request):
    packaging_list = Packaging.objects.all().order_by('name')
    packaging_to_edit = None

    if 'edit' in request.GET:
        packaging_to_edit = get_object_or_404(Packaging, id=request.GET['edit'])

    if request.method == "POST":
        action = request.POST.get('action')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        if action is None:
            Packaging.objects.create(name=name, quantity=quantity)
            Log.objects.create(
                user=request.user,
                action=f"added packaging '{name}'",
                timestamp=timezone.now()
            )
        elif action == "update_packaging":
            packaging_id = request.POST.get('packaging_id')
            pack = get_object_or_404(Packaging, id=packaging_id)
            pack.name = name
            pack.quantity = quantity
            pack.save()
            Log.objects.create(
                user=request.user,
                action=f"updated packaging '{name}'",
                timestamp=timezone.now()
            )
        return redirect('packaging')

    return render(request, 'dashboard/packaging.html', {
        'packaging_list': packaging_list,
        'packaging_to_edit': packaging_to_edit
    })

def delete_packaging(request, id):
    packaging = Packaging.objects.get(pk=id)
    packaging.delete()
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
