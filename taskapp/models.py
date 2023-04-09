from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
# taskapp

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Item(models.Model):
    text = models.TextField(max_length=500, unique=False)
    due_date = models.DateField()
    status = models.BooleanField(editable=True)
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-due_date']
