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
    amount_list = request.data.get('amount')
    
    if not amount_list:
        return Response({'detail': 'Montant invalide'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = Decimal(amount_list)
    except ValueError:
        return Response({'detail': 'Montant invalide'}, status=status.HTTP_400_BAD_REQUEST)

    if account.solde < amount:
        return Response({'detail': 'Solde insuffisant'}, status=status.HTTP_400_BAD_REQUEST)

    # Retirer le montant du solde du compte
    account.solde -= amount
    account.save()

    serializer = BankAccountSerializer(account)
    return Response(serializer.data)