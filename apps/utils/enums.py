from django.db.models import TextChoices


class RoleType(TextChoices):
    ADMIN = 'admin', 'admin'
    MANAGER = 'manager', 'manager'
    WORKER = 'worker', 'worker'
    PARTNER = 'partner', 'partner'