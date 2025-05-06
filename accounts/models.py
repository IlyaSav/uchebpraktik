from django.db import models

class Beetle(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True, null=True, help_text="CSS class for the beetle icon, e.g. 'fas fa-bug'")
    beetle_image = models.ImageField(upload_to='beetle_images/', blank=True, null=True, help_text="Image of the beetle")
    description = models.TextField(help_text="Solution for getting rid of this beetle at home")

    def __str__(self):
        return self.name
