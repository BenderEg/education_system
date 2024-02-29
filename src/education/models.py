import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Now


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField("created_at",
                                      auto_now_add=True, db_default=Now()
                                      )
    updated_at = models.DateTimeField("updated_at",
                                      auto_now=True, db_default=Now()
                                      )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Product(UUIDMixin, TimeStampedMixin):

    creator_id = models.UUIDField(blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    starting_date = models.DateTimeField(blank=False, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                blank=False, null=False)
    min_students = models.IntegerField(default=3,
                                       help_text="Enter minimum number of students in group",
                                       validators=[MinValueValidator(0), MaxValueValidator(5)])
    max_students = models.IntegerField(default=6,
                                       help_text="Enter maximum number of students in group",
                                       validators=[MinValueValidator(6), MaxValueValidator(20)])

    def __str__(self) -> str:
        return self.name

class Lesson(UUIDMixin, TimeStampedMixin):

    name = models.CharField(max_length=100, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    link = models.URLField(blank=False, null=False)