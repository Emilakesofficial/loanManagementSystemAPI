from django.urls import path
from .views import *

urlpatterns = [
    path('request-loan/', LoanRequestView.as_view()),
    path('loan-details/', LoanDetailView.as_view()),
    path('repay-loan/', RepaymentView.as_view()),
    path('loan-balance/', LoanBalanceView.as_view()),
    path('approve/<int:loan_id>/', LoanApprovalView.as_view()),
]