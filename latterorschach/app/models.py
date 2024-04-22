from django.db import models
from django import utils
import datetime
import uuid

from django.contrib.auth.models import User

# Create your models here.

class Latte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular latte")

    date = models.DateField(max_length=200,
                            unique=True,
                            default=utils.timezone.now)

    img_url = models.URLField(help_text="link to image on CDN or public internet")

    user = models.ForeignKey(User,
                             default=1,
                             null=True,
                             on_delete=models.SET_NULL
                             )

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('latte', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.date)

class Interpretation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                        help_text="Unique ID for this particular interpretation")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='replies')

    latte = models.ForeignKey(Latte,
                               on_delete=models.CASCADE,
                               related_name='latte')

    user = models.ForeignKey(User,
                            default=1,
                            null=True,
                            on_delete=models.SET_NULL
                            )

# class Like(models.Model):

#     interpretation = models.ForeignKey(Interpretation,
#                                on_delete=models.CASCADE,
#                                null=True,
#                                blank=True,
#                                related_name='replies')

#     user = models.ForeignKey(User,
#                         default=1,
#                         null=True,
#                         on_delete=models.SET_NULL
#                         )
