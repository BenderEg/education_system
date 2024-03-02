from typing import Iterable
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
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

    def __str__(self) -> str:
        return self.name

    def model_dump(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "link": self.link,
            "product": self.product.id
        }


class Group(UUIDMixin, TimeStampedMixin):

    name = models.CharField(max_length=100, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class UserProduct(UUIDMixin):

    user_id = models.UUIDField(blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)

    # add unique constraint

    def save(self, product_id: uuid.UUID, user_id: uuid.UUID, *args, **kwargs):
        super(UserProduct, self).save(*args, **kwargs)
        product = Product.objects.get(id=product_id)
        groups = Group.objects.raw("SELECT education_group.id, education_group.name, \
                                    count(education_usergroup.user_id) as students \
                                    FROM education_usergroup RIGHT \
                                    JOIN education_group \
                                    ON education_group.id = education_usergroup.group_id \
                                    GROUP BY education_group.id \
                                    ORDER BY students DESC")
        groups_ids = [ele.id for ele in groups]
        availible_groups = list(filter(lambda x: x.students < product.max_students, groups))
        if availible_groups:
            # add user to the most filled group
            new = UserGroup(group_id=availible_groups[0].id, user_id=user_id)
            new.save()
        else:
            # create new group if all groups are filled
            with transaction.atomic():
                new_group = Group(name="autogenerate", product_id=product_id)
                new_group.save()
                new = UserGroup(group_id=new_group.id, user_id=user_id)
                new.save()
                groups_ids.append(new_group.id)
        # reorginize students in groups
        users = UserGroup.objects.filter(group_id__in=groups_ids).only("id")
        if len(users) <= product.min_students:
            return
        with transaction.atomic():
            i = 1
            while True:
                if len(users)/i <= product.max_students:
                    choosen_groups = groups_ids[:i]
                    part = len(users)//i
                    new_lines = []
                    j = 0
                    for ele in choosen_groups:
                        lines = [(value.id, ele) for value in users[j:j+part]]
                        new_lines.extend(lines)
                        j += part
                    k = 0
                    for ele in users[j:]:
                        new_lines.append((ele.id, choosen_groups[k]))
                        k += 1
                    UserGroup.objects.filter(group_id__in=groups_ids).delete()
                    UserGroup.objects.bulk_create(
                        [UserGroup(user_id=ele[0], group_id=ele[1]) for ele in new_lines]
                        )
                    break
                i += 1

class UserGroup(UUIDMixin):

    user_id = models.UUIDField(blank=False, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, null=False)