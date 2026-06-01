from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class StudentGroup(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Группа"
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class Company(models.Model):
    representative = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_profile"
    )

    name = models.CharField(max_length=255)

    inn = models.CharField(
        max_length=12,
        unique=True
    )

    ogrn = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True
    )

    address = models.TextField(blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
    )

    chat_enabled = models.BooleanField(
        default=True
    )

    external_contact = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def clean(self):
        if (
            self.representative
            and self.representative.role != "company"
        ):
            raise ValidationError(
                "Представителем может быть только пользователь роли 'Предприятие'."
            )

    def __str__(self):
        return self.name


class Practice(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="practices"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    requirements = models.TextField(
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    places = models.PositiveIntegerField(
        default=1
    )

    is_archived = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )
    
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title


class ApplicationStatus(models.TextChoices):
    PENDING = "pending", "На рассмотрении"
    APPROVED = "approved", "Одобрена"
    REJECTED = "rejected", "Отклонена"
    CANCELLED = "cancelled", "Отменена"


class Application(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    practice = models.ForeignKey(
        Practice,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    completed = models.BooleanField(
        default=False
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "practice")

    def clean(self):
        active_statuses = [
            ApplicationStatus.PENDING,
            ApplicationStatus.APPROVED
        ]

        exists = Application.objects.filter(
            student=self.student,
            status__in=active_statuses
        ).exclude(pk=self.pk)

        if exists.exists():
            raise ValidationError(
                "У студента уже есть активная заявка."
            )

    def __str__(self):
        return f"{self.student} → {self.practice}"
    
    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

class DocumentTemplate(models.Model):
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to="templates/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class DocumentType(models.TextChoices):
    AGREEMENT = "agreement", "Договор"
    REPORT = "report", "Отчет"
    REVIEW = "review", "Отзыв"
    OTHER = "other", "Другое"

class DocumentStatus(models.TextChoices):
    UPLOADED = "uploaded", "Загружен"
    APPROVED = "approved", "Проверен"

class Document(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    
    title = models.CharField(
        max_length=255
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices
    )

    file = models.FileField(
        upload_to="documents/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.UPLOADED
    )


class ChatMessage(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        
class TeacherGroup(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="curated_groups"
    )

    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name="teachers"
    )

    class Meta:
        unique_together = ("teacher", "group")
        
    def clean(self):
        if self.teacher.role != "department":
            raise ValidationError(
                "Куратором группы может быть только представитель от кафедры."
            )

    def __str__(self):
        return f"{self.teacher} - {self.group}"