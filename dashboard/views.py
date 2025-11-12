from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Flavor, Ingredient, Topping, Packaging, Log

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
          # 🧾 Log the flavor addition
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

    # Check if user is editing
    if 'edit' in request.GET:
        packaging_to_edit = get_object_or_404(Packaging, id=request.GET['edit'])

    if request.method == "POST":
        action = request.POST.get('action')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        # 🟢 ADD NEW PACKAGING
        if action is None:
            Packaging.objects.create(name=name, quantity=quantity, price=price)

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
            pack.price = price
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

# ----------------- Inventory View -----------------
@login_required
def inventory(request):
    # Gather stock alerts for all dashboards
    stock = {
        'flavors': Flavor.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'toppings': Topping.objects.all(),
        'packaging': Packaging.objects.all(),
    }
    return render(request, 'dashboard/inventory.html', {'stock': stock})

# ----------------- Restock Functions -----------------
@login_required
def restock_flavor(request, id):
    flavor = get_object_or_404(Flavor, id=id)
    flavor.quantity += 10  # example restock amount
    flavor.save()
    return redirect('inventory')

@login_required
def restock_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    ingredient.quantity += 10
    ingredient.save()
    return redirect('inventory')

@login_required
def restock_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    topping.quantity += 10
    topping.save()
    return redirect('inventory')

@login_required
def restock_packaging(request, id):
    pack = get_object_or_404(Packaging, id=id)
    pack.quantity += 10
    pack.save()
    return redirect('inventory')

# ----------------- LOG HISTORY -----------------
@login_required
def log_history(request):
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/log_history.html', {'logs': logs})
