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
def toppings(request, topping_id=None):
    topping_to_edit = None

    if topping_id:
        topping_to_edit = get_object_or_404(Topping, id=topping_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if topping_to_edit:
            topping_to_edit.name = name
            topping_to_edit.price = price
            topping_to_edit.stock = stock
            topping_to_edit.save()

            Log.objects.create(
                user=request.user,
                action=f"updated topping '{name}'",
                timestamp=timezone.now()
            )
        else:
            if name and price and stock:
                Topping.objects.create(
                    name=name,
                    price=price,
                    stock=stock
                )

                Log.objects.create(
                    user=request.user,
                    action=f"added topping '{name}'",
                    timestamp=timezone.now()
                )

        return redirect('toppings')

    all_toppings = Topping.objects.all()
    return render(request, 'dashboard/toppings.html', {
        'toppings': all_toppings,
        'topping_to_edit': topping_to_edit
    })


def delete_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    name = topping.name
    topping.delete()

    Log.objects.create(
        user=request.user,
        action=f"deleted topping '{name}'",
        timestamp=timezone.now()
    )

    return redirect('toppings')


# ----------------- PACKAGING CRUD -----------------
def packaging(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        cost = request.POST.get('cost')
        quantity = request.POST.get('quantity')

        if type and cost and quantity is not None:
            Packaging.objects.create(
                type=type,
                cost=cost,
                quantity=int(quantity)
            )

            Log.objects.create(
                user=request.user,
                action=f"added packaging '{type}'",
                timestamp=timezone.now()
            )

        return redirect('packaging')

    packaging_list = Packaging.objects.all()
    return render(request, 'dashboard/packaging.html', {'packaging_list': packaging_list})


def update_packaging(request, id):
    pack = get_object_or_404(Packaging, id=id)

    if request.method == 'POST':
        pack.type = request.POST.get('type')
        pack.cost = request.POST.get('cost')
        pack.quantity = int(request.POST.get('quantity'))
        pack.save()

        Log.objects.create(
            user=request.user,
            action=f"updated packaging '{pack.type}'",
            timestamp=timezone.now()
        )

        return redirect('packaging')

    packaging_list = Packaging.objects.all()
    return render(request, 'dashboard/packaging.html', {
        'packaging_to_edit': pack,
        'packaging_list': packaging_list
    })


def delete_packaging(request, id):
    pack = get_object_or_404(Packaging, id=id)
    type_name = pack.type
    pack.delete()

    Log.objects.create(
        user=request.user,
        action=f"deleted packaging '{type_name}'",
        timestamp=timezone.now()
    )

    return redirect('packaging')


# ----------------- LOG HISTORY -----------------
def log_history(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'log_history.html', {'logs': logs})
