from .models import Flavor
from django.db.models import F, Q

def stock_alerts(request):
    """
    Provides global stock alerts for Flavors:
    - Run Out: quantity = 0
    - Critical: quantity <= critical_threshold (>0)
    - Low: quantity <= low_threshold (> critical_threshold)
    """
    runout_flavors = Flavor.objects.filter(quantity=0)
    critical_flavors = Flavor.objects.filter(quantity__lte=F('critical_threshold'), quantity__gt=0)
    low_flavors = Flavor.objects.filter(quantity__lte=F('low_threshold'), quantity__gt=F('critical_threshold'))

    return {
        'runout_flavors': runout_flavors,
        'critical_flavors': critical_flavors,
        'low_flavors': low_flavors,
    }
