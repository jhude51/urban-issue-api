from django.db import models

class Issue(models.Model):
    REPORTER_CHOICES = [
        ("vendor", "Vendor"),
        ("citizen", "Citizen"),
    ]

    CATEGORY_CHOICES = [
        ("road", "Road"),
        ("drainage", "Drainage"),
        ("streetlight", "Streetlight"),
        ("traffic", "Traffic"),
        ("waste", "Waste"),
        ("water", "Water"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("reported", "Reported"),
        ("acknowledged", "Acknowledged"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    location = models.CharField(max_length=255)

    reporter = models.CharField(
        max_length=20,
        choices=REPORTER_CHOICES,
        default="citizen",
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="reported",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return self.title
