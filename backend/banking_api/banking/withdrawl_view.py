from decimal import Decimal
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BankAccount
from .serializer import BankAccountSerializer
from rest_framework.decorators import api_view

@api_view(['PUT'])
def withdraw_view(request, pk):
    try:
        account = BankAccount.objects.get(pk=pk)
    except BankAccount.DoesNotExist:
        return Response({'detail': 'Compte introuvable'}, status=status.HTTP_404_NOT_FOUND)

    # Extraire le montant du request.data['amount']
    amount_list = request.data.getlist('amount', [])
    
    if not amount_list:
        return Response({'detail': 'Montant invalide'}, status=status.HTTP_400_BAD_REQUEST)

    # Convertir la première valeur de la liste en Decimal
    try:
        amount = Decimal(amount_list[0])
    except ValueError:
        return Response({'detail': 'Montant invalide'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si le solde est suffisant pour le retrait
    if account.solde < amount:
        return Response({'detail': 'Solde insuffisant'}, status=status.HTTP_400_BAD_REQUEST)

    # Retirer le montant du solde du compte
    account.solde -= amount
    account.save()

    serializer = BankAccountSerializer(account)
    return Response(serializer.data)