from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = "student", "Студент"
    COMPANY = "company", "Предприятие"
    DEPARTMENT = "department", "Кафедра"
    ADMIN = "admin", "Администратор"


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT
    )

    middle_name = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    group = models.ForeignKey(
        "core.StudentGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    @property
    def profile_completed(self):
        return bool(self.phone and self.email)
    
    @property
    def has_active_practice(self):
        return self.applications.filter(
            status='approved'
        ).exists()

    @property
    def full_name(self):
        return (
            f"{self.last_name} "
            f"{self.first_name} "
            f"{self.middle_name}"
        ).strip()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"