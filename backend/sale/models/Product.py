from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=155)
    value = models.FloatField()
    imagePath = models.ImageField(upload_to="assets/")

    def __str__(self):
        return f"{self.name} {self.value}"
