from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.utils import timezone

# Create your models here.
CATEGORY_CHOICES=(
    ('S','Secondhand'),
    ('N','New')
    )


class Item(models.Model):
    title= models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True, null=True)
    category= models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    description = models.TextField(max_length=250)
    image=models.ImageField(upload_to='ecommerce/',null=True, blank=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    contact=models.CharField( max_length=12, validators=[MinLengthValidator(10)], verbose_name="Mobile No")
   

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('product', kwargs={
            'pk':self.pk
            })

    def get_add_to_cart_url(self):
     return reverse('add_to_cart', kwargs={
            'pk':self.pk
            })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'pk':self.pk
            })

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    
    ordered=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{ self.item.title }"

    def item_price(self):
        return self.item.price
    def discount_item_price(self):
        return self.item.discount_price
    def get_amount_saved(self):
        return self.item_price()-self.discount_item_price()
    def get_final_price(self):
        if self.item.discount_price:
            return self.discount_item_price()
        return self.item_price()
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items =models.ManyToManyField(OrderItem)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('product',kwargs={'pk': self.pk})


