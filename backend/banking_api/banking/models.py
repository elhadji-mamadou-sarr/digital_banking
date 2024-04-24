from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    numero_compte = models.CharField(max_length=20, unique=True)  
    client = models.ForeignKey(User, on_delete=models.CASCADE)  
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Solde initial du compte

    def __str__(self):
        return f"Bank Account {self.numero_compte} - Owner: {self.client.username}"
    
    @property
    def get_balance(self):
        return "%.2f"%(float(self.solde))
