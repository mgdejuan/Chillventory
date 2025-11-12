from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import Log, Flavor, Ingredient, Topping, Packaging
from .models import LogHistory  # in sidebar/views.py

# Home page (requires login)
@login_required
def home(request):
    recent_logs = LogHistory.objects.all().order_by('-date_and_time')[:10]
    return render(request, 'sidebar/home.html', {
        'recent_logs': recent_logs
    })



# ----------------- Inventory View -----------------
@login_required
def inventory(request):
    # Gather stock for all categories
    stock = {
        'flavors': Flavor.objects.all(),
        'ingredients': Ingredient.objects.all(),
        'toppings': Topping.objects.all(),
        'packaging': Packaging.objects.all(),
    }
    # Render the template from sidebar/templates/sidebar/
    return render(request, 'sidebar/inventory.html', {'stock': stock})

def notifications(request):
    return render(request, 'sidebar/notifications.html')

# Log history page
@login_required
def log_history(request):
    return render(request, 'sidebar/log_history.html')

# About page
@login_required
def about(request):
    return render(request, 'sidebar/about.html')

@login_required
def logout_view(request):
    return render(request, 'logout_view.html')


