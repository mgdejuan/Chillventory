from django.shortcuts import render, redirect, get_object_or_404
from .models import Flavor, Ingredient, Topping, Packaging
from datetime import datetime

def dashboard(request):
    return render(request, 'dashboard/home.html')

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
        expiration_date_str = request.POST.get('expiration_date')

        # ✅ Convert expiration_date string to a Python date
        expiration_date = None
        if expiration_date_str:
            try:
                expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
            except ValueError:
                expiration_date = None

        if action == 'update_flavor':
            flavor = Flavor.objects.get(id=request.POST.get('flavor_id'))
            flavor.name = name
            flavor.price = price
            flavor.quantity = quantity
            flavor.expiration_date = expiration_date
            flavor.save()
        else:
            Flavor.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                expiration_date=expiration_date
            )

        return redirect('flavors')

    return render(request, 'dashboard/flavors.html', {
        'flavors': flavors,
        'flavor_to_edit': flavor_to_edit
    })

# ----- INGREDIENTS CRUD -----
def ingredients(request, ingredient_id=None):
    ingredient_to_edit = None

    # If editing
    if ingredient_id:
        ingredient_to_edit = get_object_or_404(Ingredient, id=ingredient_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        if ingredient_to_edit:
            # Update existing ingredient
            ingredient_to_edit.name = name
            ingredient_to_edit.quantity = quantity
            ingredient_to_edit.save()
        else:
            # Add new ingredient
            if name and quantity:
                Ingredient.objects.create(name=name, quantity=quantity)

        return redirect('ingredients')

    ingredients_list = Ingredient.objects.all()

    context = {
        'ingredients': ingredients_list,
        'ingredient_to_edit': ingredient_to_edit
    }

    return render(request, 'dashboard/ingredients.html', context)


def delete_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    ingredient.delete()
    return redirect('ingredients')


# ----- TOPPINGS CRUD -----
def toppings(request, topping_id=None):
    topping_to_edit = None

    # If editing
    if topping_id:
        topping_to_edit = get_object_or_404(Topping, id=topping_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if topping_to_edit:
            # Update existing topping
            topping_to_edit.name = name
            topping_to_edit.price = price
            topping_to_edit.stock = stock
            topping_to_edit.save()
        else:
            # Add new topping
            if name and price and stock:
                Topping.objects.create(
                    name=name,
                    price=price,
                    stock=stock
                )

        return redirect('toppings')

    all_toppings = Topping.objects.all()
    context = {
        'toppings': all_toppings,
        'topping_to_edit': topping_to_edit
    }
    return render(request, 'dashboard/toppings.html', context)


def delete_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    topping.delete()
    return redirect('toppings')



def delete_topping(request, id):
    topping = get_object_or_404(Topping, id=id)
    topping.delete()
    return redirect('toppings')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Packaging

# ----------------- PACKAGING CRUD -----------------

def packaging(request):
    """
    Display packaging list and handle adding new packaging.
    """
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
        return redirect('packaging')

    packaging_list = Packaging.objects.all()
    return render(request, 'dashboard/packaging.html', {'packaging_list': packaging_list})


def update_packaging(request, id):
    """
    Edit an existing packaging item.
    """
    pack = get_object_or_404(Packaging, id=id)

    if request.method == 'POST':
        pack.type = request.POST.get('type')
        pack.cost = request.POST.get('cost')
        pack.quantity = int(request.POST.get('quantity'))
        pack.save()
        return redirect('packaging')

    # Pass both the item to edit and the full list to reuse the template
    packaging_list = Packaging.objects.all()
    return render(request, 'dashboard/packaging.html', {
        'packaging_to_edit': pack,
        'packaging_list': packaging_list
    })


def delete_packaging(request, id):
    """
    Delete a packaging item.
    """
    pack = get_object_or_404(Packaging, id=id)
    pack.delete()
    return redirect('packaging')
