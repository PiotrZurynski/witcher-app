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
    def __str__(self):
        return self.name + " " + self.realm

class Monster(models.Model):
    CATEGORY_CHOICES=[
        ("BES","Bestie"),
        ("DRA","Drakonidy"),
        ("HYB","Hybrydy"),
        ("INS","Insektoidy"),
        ("ISTM","Istoty Magiczne"),
        ("ISTP","Istoty przeklęte"),
        ("OGR","Ogrowate"),
        ("REL","Relikty"),
        ("TRU","Trupojady"),
        ("UPI","Upiory"),
        ("WAM","Wampiry"),
        ("UNK","Nieznane")
    ]
    name=models.CharField(max_length=70)
    category=models.CharField(max_length=5,choices=CATEGORY_CHOICES,default="TRU")
    description=models.TextField(blank=True)

    class Meta:
        ordering=["category","name"]

    def __str__(self):
        return self.category + " - " + self.name