from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LogHistory, Inventory

# Home page (requires login)
@login_required
def home(request):
    recent_logs = LogHistory.objects.all().order_by('-date_and_time')[:10]
    return render(request, 'sidebar/home.html', {
        'recent_logs': recent_logs
    })

# Inventory page (requires login)
@login_required
def inventory(request):
    inventory_data = [
        {'name': 'Sprinkles', 'category': 'Toppings', 'stock': 5, 'updated_at': '2025-10-15'},
        {'name': 'Vanilla Syrup', 'category': 'Flavors', 'stock': 12, 'updated_at': '2025-10-12'},
    ]
    return render(request, 'sidebar/inventory.html', {'inventory': inventory_data})

# Notifications page
@login_required
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

def inventory_view(request):
    inventory = Inventory.objects.all().order_by('category', 'product_name')
    return render(request, 'sidebar/inventory.html', {'inventory': inventory})