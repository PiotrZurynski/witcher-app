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
        return self.name + " " + self.realm.name

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
        return self.get_category_display() + " - " + self.name
    
class Contract(models.Model):
    CURRENCY_CHOICES=[
        ("KRN","Korony"),
        ("ORN","Oreny"),
        ("FLO","Floreny"),
    ]
    STATE_CHOICES=[
        ("OPN","Aktywne"),
        ("TKN","Przyjęte"),
        ("DON","Zakończone"),
        ("CAN","Anulowane"),
    ]
    title=models.CharField(max_length=150)
    description=models.TextField(blank=True)
    realm=models.ForeignKey(Realm,on_delete=models.CASCADE)
    town=models.ForeignKey(Town,on_delete=models.CASCADE)
    monster=models.ForeignKey(Monster,on_delete=models.CASCADE)
    currency=models.CharField(max_length=3,choices=CURRENCY_CHOICES,default="KRN")
    reward=models.IntegerField(default=0)
    state=models.CharField(max_length=3,choices=STATE_CHOICES,default="OPN")

    time_created=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=["-time_created"]
    
    def __str__(self):
        return self.title +" - "+self.realm.name +" - "+self.town.name