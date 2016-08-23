from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, **kwargs):
        if kwargs is not None:
            errors = {}
        if len(kwargs['first_name']) < 1:
            errors['first_name'] = "First Name is required"
        elif len(kwargs['last_name']) < 1:
            errors['first_name'] = "First Name is required"
        elif len(kwargs['first_name']) < 2:
            errors['first_name'] = "Name must be at least 2 characters"
        elif len(kwargs['last_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters"
#        elif str.isnumeric(kwargs['first_name']):
#            errors.append('Only Letters Please!')
#        elif not uchr.isalpha(kwargs['last_name']):
#            errors.append('Only Letters Please!')
        elif len(kwargs['email']) < 1:
            errors['email'] = "Please enter Email!"
        elif not EMAIL_REGEX.match(kwargs['email']):
            errors['email'] = "Email is not valid!"
        elif len(kwargs['password']) < 1:
            errors['password'] = "Please enter Password"
        elif len(kwargs['password_conf']) < 1:
            errors['password_conf'] = "Please enter Password"
        elif len(kwargs['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        elif len(kwargs['password_conf']) < 8:
            errors['password_conf'] = "Password must be at least 8 characters."
        elif not kwargs['password'] == kwargs['password_conf']:
            errors['password_conf'] = "Passwords must match!"
        if len(errors) > 0:
            return (False, errors)
        else:
            pw_hash = bcrypt.hashpw(kwargs['password'].encode(), bcrypt.gensalt())
            print pw_hash
            user = User.userMgr.create(first_name=kwargs['first_name'], last_name=kwargs['last_name'], email=kwargs['email'], pw_hash=pw_hash)
            user.save()
            return (True, user)

    def login(self, **kwargs):
        if kwargs is not None:
            errors = {}
            if len(kwargs['password']) == 0:
                errors['password'] = "Please enter a Password"
            if len(kwargs['email']) == 0:
                errors['email'] = "Please enter an Email"
            if len(errors) != 0:
                return (False, errors)
            else:
                user = User.userMgr.filter(email=kwargs['email'])
                if not user:
                    errors['user'] = "Email/Password Not Found"
                    return (False, errors)
                else:
                    if bcrypt.checkpw(kwargs['password'].encode('utf-8'), user[0].pw_hash.encode('utf-8')):
                        print ("It Matches!")
                        return (True, user[0])
                    else:
                        errors['user'] = "Email/Password Combination Not Found"
                        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    pw_hash = models.CharField(max_length=60)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    userMgr = UserManager()
