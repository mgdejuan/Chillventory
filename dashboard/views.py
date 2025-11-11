from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Flavor, Ingredient, Topping, Packaging, Log
from datetime import datetime


# ----------------- DASHBOARD -----------------
def dashboard(request):
    return render(request, 'dashboard/home.html')


# ----------------- FLAVORS CRUD -----------------
def flavors(request):
    flavors = Flavor.objects.all().order_by('name')
    flavor_to_edit = None

    if 'edit' in request.GET:
        flavor_to_edit = Flavor.objects.get(id=request.GET['edit'])

    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        expiration_date = request.POST.get('expiration_date')

        if action == 'update_flavor':
            flavor = Flavor.objects.get(id=request.POST.get('flavor_id'))
            flavor.name = name
            flavor.price = price
            flavor.quantity = quantity
            flavor.expiration_date = expiration_date
            flavor.save()

            # 🧾 Log update
            Log.objects.create(
                user=request.user,
                action=f"updated flavor '{name}'",
                timestamp=timezone.now()
            )

        else:
            Flavor.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

            # 🧾 Log add
            Log.objects.create(
                user=request.user,
                action=f"added flavor '{name}'",
                timestamp=timezone.now()
            )

        return redirect('flavors')

    return render(request, 'dashboard/flavors.html', {
        'flavors': flavors,
        'flavor_to_edit': flavor_to_edit
    })


def delete_flavor(request, delete_id):
    flavor = get_object_or_404(Flavor, id=delete_id)
    name = flavor.name
    flavor.delete()

    # 🧾 Log delete
    Log.objects.create(
        user=request.user,
        action=f"deleted flavor '{name}'",
        timestamp=timezone.now()
    )

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

            # 🧾 Log update
            Log.objects.create(
                user=request.user,
                action=f"updated ingredient '{name}'",
                timestamp=timezone.now()
            )

        else:
            Ingredient.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

            # 🧾 Log add
            Log.objects.create(
                user=request.user,
                action=f"added ingredient '{name}'",
                timestamp=timezone.now()
            )

        return redirect('ingredients')

    return render(request, 'dashboard/ingredients.html', {
        'ingredients': ingredients,
        'ingredient_to_edit': ingredient_to_edit
    })


def delete_ingredient(request, delete_id):
    ingredient = get_object_or_404(Ingredient, id=delete_id)
    name = ingredient.name
    ingredient.delete()

    # 🧾 Log delete
    Log.objects.create(
        user=request.user,
        action=f"deleted ingredient '{name}'",
        timestamp=timezone.now()
    )

    return redirect('ingredients')



# ----------------- TOPPINGS CRUD -----------------
def toppings(request):
    toppings = Topping.objects.all().order_by('name')
    topping_to_edit = None

    # If user clicks “Edit”
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

            # 🧾 Log update
            Log.objects.create(
                user=request.user,
                action=f"updated topping '{name}'",
                timestamp=timezone.now()
            )

        else:
            Topping.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

            # 🧾 Log add
            Log.objects.create(
                user=request.user,
                action=f"added topping '{name}'",
                timestamp=timezone.now()
            )

        return redirect('toppings')

    return render(request, 'dashboard/toppings.html', {
        'toppings': toppings,
        'topping_to_edit': topping_to_edit
    })


def delete_topping(request, id):
    topping = Topping.objects.get(id=id)
    topping.delete()
    return redirect('toppings')

# ----------------- PACKAGING CRUD -----------------
def add_packaging(request):
    packaging_list = Packaging.objects.all().order_by('name')
    packaging_to_edit = None

    # Check if user is editing
    if 'edit' in request.GET:
        packaging_to_edit = get_object_or_404(Packaging, id=request.GET['edit'])

    if request.method == "POST":
        action = request.POST.get('action')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        # 🟢 ADD NEW PACKAGING
        if action is None:
            Packaging.objects.create(name=name, quantity=quantity)

            # 🧾 Log add
            Log.objects.create(
                user=request.user,
                action=f"added packaging '{name}'",
                timestamp=timezone.now()
            )

        # 🟡 UPDATE PACKAGING
        elif action == "update_packaging":
            packaging_id = request.POST.get('packaging_id')
            pack = get_object_or_404(Packaging, id=packaging_id)
            pack.name = name
            pack.quantity = quantity
            pack.save()

            # 🧾 Log update
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


# ----------------- DELETE PACKAGING -----------------
def delete_packaging(request, id):
    packaging = Packaging.objects.get(pk=id)
    packaging.delete()
    return redirect('packaging')

    # 🧾 Log delete
    Log.objects.create(
        user=request.user,
        action=f"deleted packaging '{name}'",
        timestamp=timezone.now()
    )

    return redirect('packaging')

# ----------------- LOG HISTORY -----------------
def log_history(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'log_history.html', {'logs': logs})
