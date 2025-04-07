from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLES_CHOICE = (
        ('borrower', 'Borrower'),
        ('admin', 'Admin'),
    )
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLES_CHOICE, default='borrower')
    loan_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=False, blank=False)
    is_email_verified = models.BooleanField(default=False)
    
    def update_loan_balance(self):
        active_loan = self.loans.filter(status="approved").first()  
        if active_loan:
            total_paid = sum(active_loan.repayments.values_list("amount_paid", flat=True))
            remaining_balance = active_loan.total_amount_due - total_paid

            if remaining_balance <= 0:
                active_loan.status = "paid"
                active_loan.save()
    def __str__(self):
        return self.user.username
