import django_filters
from .models import BankAccount

class BankAccountFilter(django_filters.FilterSet):
    class Meta:
        model = BankAccount
        fields = {
            'numero_compte': ['exact', 'icontains'],
            'client__username': ['exact', 'icontains'],
            'solde': ['exact', 'gte', 'lte'],
        }
