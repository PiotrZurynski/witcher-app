from django.db import models

# Create your models here.
class Realm(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)

    class Meta:
        ordering=["name"]
    def __str__(self):
        return self.name

class Town(models.Model):
    name=models.CharField(max_length=100)
    realm=models.ForeignKey(Realm,on_delete=models.CASCADE)

    class Meta:
        ordering=["realm", "name"]    