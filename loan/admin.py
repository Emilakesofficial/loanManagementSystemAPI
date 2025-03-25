from django.contrib import admin
from .models import Loan, Repayment

admin.site.register(Loan)
admin.site.register(Repayment)
