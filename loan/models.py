from django.db import models
from user.models import UserProfile
from django.utils.timezone import now

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="loans")  # A user can have only one active loan
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Loan amount
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)  # Fixed 5% interest
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Loan + Interest
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total amount due (loan amount + 5% interest)
        self.total_amount_due = self.amount + (self.amount * self.interest_rate / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan for {self.user.user.username} - {self.status}"

class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(default=now)

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.loan.user.user.username}"
