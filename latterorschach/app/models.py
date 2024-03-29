from django.db import models
import datetime

# Create your models here.

class Latte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular latte")

    date = models.DateField(max_length=200,
                            unique=True,
                            default=datetime.date.today())

    img_url = models.URLField(help_text="link to image on CDN or public internet")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('latte', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.date

class Interpretation():
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                        help_text="Unique ID for this particular interpretation")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='replies')

    
    parent_id = models.UUIDField()