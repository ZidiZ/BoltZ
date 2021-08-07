from django.db import models
from datetime import date
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
'''
Check installed apps for phonenumber_field, for contact number
#from phonenumber_field.modelfields import PhoneNumberField

Check if database can be changed to pg which supports Composite field for Address
#from django_pg import models
'''




# class Address(CompositeField):
#     line1 = models.CharField(max_length=128)
#     line2 = models.CharField(max_length=128, blank=True, null=True)
#     postcode = models.CharField()
#     city = models.CharField(max_length=32)

class Shelter(models.Model):
    name = models.CharField(max_length=128, unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    #address = Address()
    address = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Shelter, self).save(*args, **kwargs)

    #Modify to show only those animals that are currently in shelter
    @property
    def number_of_animals(self):
        return self.animal_set.count()

    def __str__(self):
        return self.name


class Animal(models.Model):    
    #Animal can exist in database without a shelter allocated
    name = models.CharField(max_length=32, default="John Doe")

    KINDS_OF_ANIMALS_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('FISH', 'Fish'),
        ('OTHER', 'Other'),
    ]
    kind = models.CharField(max_length=10, choices=KINDS_OF_ANIMALS_CHOICES, default='DOG')

    description = models.CharField(max_length=256, blank=True)
    picture = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    date_of_arrival = models.CharField(max_length=25,blank=True, default=date.today)

    ADOPTION_CHOICES = [
        ('ADOPTED', 'Adopted'),
        ('NOT_ADOPTED', 'Waiting for a home'),
        ('REQUESTED', 'Request pending'),
        ('UNKNOWN', 'Unknown'),
    ]
    adoption_status = models.CharField(max_length=16, choices=ADOPTION_CHOICES, default='UNKNOWN')
    adoption_date = models.CharField(max_length=25,null=True, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32,default='1')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.username
    
class Fqa(models.Model):
    email = models.CharField(max_length=32)
    content = models.CharField(max_length=256)

class AdopterInfo(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    animal_id= models.IntegerField()