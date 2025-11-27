from django.db.models import TextChoices


class TaskStatus(TextChoices):
    NEW = "N", "Nowy"
    IN_PROGRESS = "P", "W toku"
    RESOLVED = "R", "Rozwiązany"
