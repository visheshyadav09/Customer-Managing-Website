from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# So when we write null=True we can select any single value from database and not get an error,for eg.-we can import customer with just name value
class Customer(models.Model):
# here we are creating one-to-one relationship between customer and user so that for every customer it stores the info of that user
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(default="messi2.jpg",null=True , blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Out Door','Out Door'),
    )
    
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name 


class Order(models.Model):
    # so this actually gives kind of like a drop down menu
    STATUS=(
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )
# So this basically helpsus create relationships,this foreign key helps us reference the external entity in this table
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    note=models.CharField(max_length=1000,null=True)
    
    def __str__(self):
        return self.product.name
# Order is child of Customer and we can use this relation to access child set
##RELATED SET EXAMPLE
'''class ParentModel(models.Model):
	name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
	parent = models.ForeignKey(Customer)
	name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
#Returns all child models related to parent
parent.childmodel_set.all()'''

''' using __ after any model name in the python shell 
we can enter the model and access its attributes like for eg. tag__name lets us 
enter tag and the access the name attribute'''