from rest_framework import serializers
from .models import Loan, Repayment

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'amount', 'interest_rate', 'total_amount_due', 'status', 'created_at']
        read_only_fields = ['status', 'total_amount_due', 'created_at']  # Prevent modification

    def create(self, validated_data):
        """Override to calculate total amount due automatically"""
        loan = Loan.objects.create(**validated_data)
        loan.total_amount_due = loan.amount + (loan.amount * loan.interest_rate / 100)
        loan.save()
        return loan

class RepaymentSerializer(serializers.ModelSerializer):
    remaining_balance = serializers.SerializerMethodField()  # Calculate remaining balance

    class Meta:
        model = Repayment
        fields = ['id', 'loan', 'amount_paid', 'date_paid', 'remaining_balance']
        read_only_fields = ['date_paid', 'remaining_balance']  # Prevent modification

    def get_remaining_balance(self, obj):
        """Calculate remaining balance after each payment"""
        total_paid = sum(obj.loan.repayments.values_list('amount_paid', flat=True))
        return obj.loan.total_amount_due - total_paid
