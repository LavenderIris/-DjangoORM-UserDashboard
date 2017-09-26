from __future__ import unicode_literals
import re
from django.db import models

ALL_LETTERS_REGEX = re.compile(r'[A-Za-z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print "firstname", postData['first_name']
        if len(postData['first_name']) < 2: 
            errors['first_name_length'] = 'First name should be more than 2 characters'
        else:
            if not postData['first_name'].isalpha():
                errors['first_name_letters'] = 'First Name should be letters only'

        if len(postData['last_name']) < 2:
            errors['last_name_length'] = 'Last name should be more than 2 characters'
        else:
            if not postData['last_name'].isalpha():
                errors['last_name_letters'] = 'Last Name should be letters only'

        if len(postData['email']) == 0 or not EMAIL_REGEX.match(postData['email']):      
            errors['email'] = 'Email is required and to be in a valid format'
        
        #  checks if email is taken
        email_taken = User.objects.filter(email = postData['email'])
        if len(email_taken) > 0 :
            errors['email taken'] = 'Email already in our database'        

        if len(postData['pw']) < 8:
            errors['pw_length'] = 'Password needs to be at least 8 characters'
        else:
            if postData['pw'] != postData['pw_confirm'] :
                errors['pw_conf'] = 'Passwords do not match'
        print "ERRORS", errors

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_level = models.IntegerField(max_length=1)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name = "messages")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    messages = models.ManyToManyField(Message, related_name = "conversations" )