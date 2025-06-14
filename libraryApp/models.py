import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Author(models.Model):
    """An author of one or more books."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Publisher(models.Model):
    """Publisher details."""
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Genre or category of books."""
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """A specific copy of a book"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    summary = models.TextField(help_text="Brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    imprint = models.CharField(max_length=200, help_text="Publisher imprint info")
    categories = models.ManyToManyField(Category, blank=True, related_name='books')
    language = models.CharField(max_length=100, blank=True, help_text="e.g. English, French")
    added_on = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('a', 'Available'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
        ('m', 'Maintenance'),
    ]

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=True,
        default='a',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Member(AbstractUser):
    # Field to track manual or previously assessed penalties
    penalty_balance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Accumulated penalties not yet paid/waived"
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    @property
    def penalty(self) -> Decimal:
        """
        Total penalty = stored balance + computed overdue fines
        for all currently overdue loans.
        """
        total = self.penalty_balance
        now = timezone.now()
        # iterate only active loans that are past due
        overdue_loans = self.loans.filter(returned_on__isnull=True, due_back__lt=now)
        for loan in overdue_loans:
            days_overdue = (now - loan.due_back).days
            total += settings.DAILY_PENALTY_RATE * days_overdue
        return total


class Loan(models.Model):
    """Record of a Book loaned to a Member."""
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='loans')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='loans')
    loaned_on = models.DateTimeField(default=timezone.now)
    due_back = models.DateTimeField(help_text="When the book should be returned")
    returned_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        unique_together = [['book', 'returned_on']]

    @property
    def is_overdue(self):
        if self.returned_on is None and timezone.now() > self.due_back:
            return True
        return False

    def __str__(self):
        return f"{self.book} loaned to {self.member}"
