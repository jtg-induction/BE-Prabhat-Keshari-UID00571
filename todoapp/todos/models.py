from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    """
        Needed fields
        - user (fk to User Model - Use AUTH_USER_MODEL from django.conf.settings)
        - name (max_length=1000)
        - done (boolean with default been false)
        - date_created (with default of creation time)
        - date_completed (set it when done is marked true)

        Add string representation for this model with todos name.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Created by") 
    name = models.CharField(max_length=1000, verbose_name="Todo")
    done = models.BooleanField(default=False, verbose_name="Todo Status")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date of Creation")
    date_completed = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Date of Completion")

    def save(self, *args, **kwargs):
        if self.done:
            self.date_completed = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
