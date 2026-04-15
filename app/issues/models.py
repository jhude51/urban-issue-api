from django.db import models

class Issue(models.Model):
    REPORTER_CHOICES = [
        ('vendor', 'Vendor'),
        ('citizen', 'Citizen'),
    ]
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    location = models.CharField(max_length=255)
    reporter = models.CharField(max_length=20, choices=REPORTER_CHOICES, default='citizen')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):        
        return self.title
