
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class IssueBook(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    issue_date = models.DateField(default=timezone.localdate)
    return_date = models.DateField()
    returned_on = models.DateField(null=True, blank=True)

    fine = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )

    is_returned = models.BooleanField(default=False)

    def calculate_fine(self):
        if self.returned_on:
            late_days = max(
                (self.returned_on - self.return_date).days, 0
            )
        else:
            late_days = max(
                (timezone.localdate() - self.return_date).days, 0
            )

        self.fine = Decimal(late_days) * Decimal('10.00')
        return self.fine

    def save(self, *args, **kwargs):
        self.calculate_fine()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} - {self.member.username}"
