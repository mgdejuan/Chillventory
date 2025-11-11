from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Flavor, Ingredient, Topping, Packaging, Log
from datetime import datetime

# ----------------- DASHBOARD -----------------
def dashboard(request):
    return render(request, 'dashboard/home.html')


# ----------------- STOCK ALERTS -----------------
def get_stock_alerts():
    """
    Check stock for Flavors, Ingredients, and Toppings.
    Returns a list of alert messages for the template.
    """
    alerts = []

    # Flavor alerts
    out_of_stock_flavors = Flavor.objects.filter(quantity=0)
    low_stock_flavors = Flavor.objects.filter(quantity__lte=5).exclude(quantity=0)  # replace 5 with your threshold

    if out_of_stock_flavors.exists():
        alerts.append(f"{out_of_stock_flavors.count()} flavor(s) are out of stock!")
    if low_stock_flavors.exists():
        alerts.append(f"{low_stock_flavors.count()} flavor(s) are low in stock!")

    # Ingredient alerts
    out_of_stock_ingredients = Ingredient.objects.filter(quantity=0)
    low_stock_ingredients = Ingredient.objects.filter(quantity__lte=5).exclude(quantity=0)

    if out_of_stock_ingredients.exists():
        alerts.append(f"{out_of_stock_ingredients.count()} ingredient(s) are out of stock!")
    if low_stock_ingredients.exists():
        alerts.append(f"{low_stock_ingredients.count()} ingredient(s) are low in stock!")

    # Topping alerts
    out_of_stock_toppings = Topping.objects.filter(quantity=0)
    low_stock_toppings = Topping.objects.filter(quantity__lte=5).exclude(quantity=0)

    if out_of_stock_toppings.exists():
        alerts.append(f"{out_of_stock_toppings.count()} topping(s) are out of stock!")
    if low_stock_toppings.exists():
        alerts.append(f"{low_stock_toppings.count()} topping(s) are low in stock!")

    return alerts


# ----------------- HOME VIEW -----------------
def home(request):
    alerts = get_stock_alerts()

    # Get recent logs (last 10)
    recent_logs = Log.objects.all().order_by('-timestamp')[:10]

    # Example: unread notifications count
    unread_notifications = 0  # replace with your logic if you track notifications

    return render(request, 'dashboard/home.html', {
        'alerts': alerts,
        'recent_logs': recent_logs,
        'unread_notifications': unread_notifications,
    })


def flavors(request):
    # Check if editing
    edit_id = request.GET.get('edit')
    if edit_id:
        flavor_to_edit = get_object_or_404(Flavor, id=edit_id)
    else:
        flavor_to_edit = None

    # Handle POST (Add / Update)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity') or 0)
        expiration_date = request.POST.get('expiration_date') or None

        if flavor_to_edit:
            flavor_to_edit.name = name
            flavor_to_edit.price = price
            flavor_to_edit.quantity = quantity
            flavor_to_edit.expiration_date = expiration_date
            flavor_to_edit.save()
        else:
            Flavor.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )
        return redirect('flavors')

    # Query all flavors
    flavors_list = Flavor.objects.all()

    # Stock alerts
    runout_flavors = flavors_list.filter(quantity=0)
    critical_flavors = [f for f in flavors_list if 0 < f.quantity <= f.critical_threshold]
    low_flavors = [f for f in flavors_list if f.critical_threshold < f.quantity <= f.low_threshold]

    return render(request, 'dashboard/flavors.html', {
        'flavors': flavors_list,
        'flavor_to_edit': flavor_to_edit,
        'runout_flavors': runout_flavors,
        'critical_flavors': critical_flavors,
        'low_flavors': low_flavors,
    })

def delete_flavor(request, delete_id):
    flavor = get_object_or_404(Flavor, id=delete_id)
    flavor.delete()
    return redirect('flavors')

# ----------------- INGREDIENTS CRUD -----------------
def ingredients(request):
    ingredients = Ingredient.objects.all().order_by('name')
    ingredient_to_edit = None

    if 'edit' in request.GET:
        ingredient_to_edit = Ingredient.objects.get(id=request.GET['edit'])

    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        expiration_date = request.POST.get('expiration_date')

        if action == 'update_ingredient':
            ingredient = Ingredient.objects.get(id=request.POST.get('ingredient_id'))
            ingredient.name = name
            ingredient.price = price
            ingredient.quantity = quantity
            ingredient.expiration_date = expiration_date
            ingredient.save()
            Log.objects.create(user=request.user, action=f"updated ingredient '{name}'", timestamp=timezone.now())
        else:
            Ingredient.objects.create(name=name, price=price, quantity=quantity, expiration_date=expiration_date)
            Log.objects.create(user=request.user, action=f"added ingredient '{name}'", timestamp=timezone.now())

        return redirect('ingredients')

    return render(request, 'dashboard/ingredients.html', {'ingredients': ingredients, 'ingredient_to_edit': ingredient_to_edit})


def delete_ingredient(request, delete_id):
    ingredient = get_object_or_404(Ingredient, id=delete_id)
    name = ingredient.name
    ingredient.delete()
    Log.objects.create(user=request.user, action=f"deleted ingredient '{name}'", timestamp=timezone.now())
    return redirect('ingredients')


# ----------------- TOPPINGS CRUD -----------------
def toppings(request):
    toppings = Topping.objects.all().order_by('name')
    topping_to_edit = None

    if 'edit' in request.GET:
        topping_to_edit = Topping.objects.get(id=request.GET['edit'])

    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        expiration_date = request.POST.get('expiration_date')

        if action == 'update_topping':
            topping = Topping.objects.get(id=request.POST.get('topping_id'))
            topping.name = name
            topping.price = price
            topping.quantity = quantity
            topping.expiration_date = expiration_date
            topping.save()
            Log.objects.create(user=request.user, action=f"updated topping '{name}'", timestamp=timezone.now())
        else:
            Topping.objects.create(name=name, price=price, quantity=quantity, expiration_date=expiration_date)
            Log.objects.create(user=request.user, action=f"added topping '{name}'", timestamp=timezone.now())

        return redirect('toppings')

    return render(request, 'dashboard/toppings.html', {'toppings': toppings, 'topping_to_edit': topping_to_edit})


def delete_topping(request, id):
    topping = Topping.objects.get(id=id)
    topping.delete()
    return redirect('toppings')


# ----------------- PACKAGING CRUD -----------------
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
            Log.objects.create(user=request.user, action=f"added packaging '{name}'", timestamp=timezone.now())
        elif action == "update_packaging":
            packaging_id = request.POST.get('packaging_id')
            pack = get_object_or_404(Packaging, id=packaging_id)
            pack.name = name
            pack.quantity = quantity
            pack.save()
            Log.objects.create(user=request.user, action=f"updated packaging '{name}'", timestamp=timezone.now())

        return redirect('packaging')

    return render(request, 'dashboard/packaging.html', {'packaging_list': packaging_list, 'packaging_to_edit': packaging_to_edit})


def delete_packaging(request, id):
    packaging = Packaging.objects.get(pk=id)
    packaging.delete()
    return redirect('packaging')


# ----------------- LOG HISTORY -----------------
@login_required
def log_history(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/log_history.html', {'logs': logs})
