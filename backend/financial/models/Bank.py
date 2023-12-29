from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
    def getCode(self):
        return str(self.code).zfill(3)