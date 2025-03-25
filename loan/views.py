from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Loan, Repayment
from .serializers import *
from user.models import UserProfile  # Import UserProfile to link loans

class LoanRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_profile = request.user.profile  

        # Get the latest loan for the user
        loan = Loan.objects.filter(user=user_profile).order_by("-created_at").first()
        
        if loan and loan.status in ["approved", "active"]:
            return Response({'error': 'You must fully repay your loan before applying for a new one'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new loan
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_profile, status='pending') 
            return Response({'Message':'Your loan request has been submitted successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoanApprovalView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)

        if loan.status != "pending":
            return Response({"error": "Loan is already processed."}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get("action")  # Approve or Reject
        if action == "approve":
            loan.status = "approved"
            loan.save()
            loan.user.update_loan_balance()  # Update user's loan balance
            return Response({"message": "Loan approved successfully."}, status=status.HTTP_200_OK)

        elif action == "reject":
            loan.status = "rejected"
            loan.save()
            return Response({"message": "Loan rejected."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action. Use 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)


    
class LoanDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            loan = Loan.objects.filter(user=request.user.profile).order_by("-created_at").first()
            if not loan:
                return Response({'Message': 'No active loan found'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = LoanSerializer(loan)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({'Message':'No active loan found'}, status=status.HTTP_400_BAD_REQUEST)

        
class RepaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_profile = request.user.profile

        # Get active loan
        loan = Loan.objects.filter(user=user_profile, status__in=["approved", "active"]).order_by("-created_at").first()
        if not loan:
            return Response({"error": "No active loan found."}, status=status.HTTP_400_BAD_REQUEST)

        amount_paid = request.data.get("amount_paid")
        if not amount_paid or float(amount_paid) <= 0:
            return Response({"error": "Invalid payment amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate remaining balance
        total_paid = sum(loan.repayments.values_list("amount_paid", flat=True))
        remaining_balance = loan.total_amount_due - total_paid

        if float(amount_paid) > remaining_balance:
            return Response({"error": "Payment exceeds remaining balance."}, status=status.HTTP_400_BAD_REQUEST)

        # Save repayment
        Repayment.objects.create(loan=loan, amount_paid=amount_paid)

        # Update user loan balance
        user_profile.update_loan_balance()

        # If fully paid, update loan status
        if remaining_balance - (amount_paid) <= 0:
            loan.status = "paid"
            loan.save()
            user_profile.update_loan_balance()  # Ensure balance is set to 0

        return Response({"message": "Repayment successful!"}, status=status.HTTP_200_OK)


class LoanBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Get the latest active loan for the user
            loan = Loan.objects.filter(user=request.user.profile, status__in=["active", "approved"]).order_by("-created_at").first()
            
            if not loan:
                return Response({"error": "No active loan found"}, status=status.HTTP_404_NOT_FOUND)

            # Calculate total repayments for this loan only
            total_paid = sum(loan.repayments.values_list('amount_paid', flat=True))

            # Calculate remaining balance
            remaining_balance = loan.total_amount_due - total_paid

            return Response({
                "message": "Loan balance retrieved successfully",
                "loan_amount": loan.amount,
                "total_amount_due": loan.total_amount_due,
                "amount_paid": total_paid,  # Only count repayments for this loan
                "remaining_balance": remaining_balance,
            }, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"error": "No active loan found"}, status=status.HTTP_404_NOT_FOUND)
