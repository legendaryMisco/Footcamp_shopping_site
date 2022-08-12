from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class Register(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          unique=True, editable=False)
    name = models.CharField(max_length=300, null=True,blank=True)
    email = models.EmailField(max_length=500, null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    username = models.CharField(max_length=300, null=True,blank=True)
    picture = models.ImageField(max_length=3000, default='user.png',upload_to='profiles/')
    contact = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    genderOption = [
        ('MALE','m'),
        ('FEMALE','f')
    ]
    gender = models.CharField(max_length=8,choices=genderOption,null=True,blank=True, default='others')
    bio = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username








