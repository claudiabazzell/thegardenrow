from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_MATCH = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def get_all_by_email(self):
        return self.order_by('email')

    def register(self, form_data):
        my_hash = bcrypt.hashpw(
            form_data['password'].encode(), bcrypt.gensalt())
        return self.create(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            password=str(my_hash).decode(),
            email=form_data['email'],
        )

    def authenticate(self, email, password):
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        user = users_with_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def validate(self, form_data):

        errors = {}
        if len(form_data['first_name']) < 1:
            errors['first_name'] = 'First Name field is required.'

        if len(form_data['last_name']) < 1:
            errors['last_name'] = 'Last Name field is required.'

        if len(form_data['email']) < 1:
            errors['email'] = 'Email field is required.'

        if not EMAIL_MATCH.match(form_data['email']):
            errors['email'] = 'Invalid Email.'

        if len(form_data['password']) < 1:
            errors['password'] = 'Password field is required.'

        if form_data['password'] != form_data['confirm']:
            errors['password'] = "Passwords do not match"

        users_with_email = self.filter(email=form_data['email'])
        if users_with_email:
            errors['email'] = 'Email already in use.'

        return errors


class ItemManager(models.Manager):

    def createItem(self, form_data):
        print('user', form_data['user'])
        return self.create(
            item_name=form_data['item'],
            quantity=form_data['quantity'],
            description=form_data['description'],
            user=form_data['user']
        )

    def validate(self, form_data):

        errors = {}
        if len(form_data['item']) < 1:
            errors['item'] = 'Field is required.'

        if len(form_data['item']) < 3:
            errors['item'] = 'An item must consist of at least 3 characters'

        if len(form_data['quantity']) < 1:
            errors['quantity'] = 'Field is required.'

        if len(form_data['description']) < 1:
            errors['description'] = 'A description must be provided!'

        if len(form_data['description']) < 3:
            errors['description'] = 'A description must consist of at least 3 characters.'

        return errors

class BlogManager(models.Manager):
  
    def createBlog(self, form_data):
        print('self', self)
        return self.create(
            title=form_data['title'],
            description=form_data['description'],
            user=form_data['user']
        )

    def validate(self, form_data):

        errors = {}
        print("start validate")
        print(form_data)
        if len(form_data['title']) < 1:
            errors['title'] = 'Field is required.'

        if len(form_data['title']) < 5:
            errors['title'] = 'A title must consist of at least 5 characters'

        if len(form_data['description']) < 1:
            errors['description'] = 'A description must be provided!'

        if len(form_data['description']) < 15:
            errors['description'] = 'A description must consist of at least 15 characters.'

        print("end validate")
        return errors


class ImageManager(models.Manager):

    def createImg(self, form_data):
        return self.create(
            title=form_data.title,
            image=form_data.image
        )


class ItemCommentManager(models.Manager):

    def createComment(self, form_data):
        return self.create(
            comment=form_data['comment'],
            user=form_data['user'],
            
            item=form_data['item']
        )
    
    def validate(self, form_data):
        errors = {}
        return errors


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    objects = ImageManager()

    def __str__(self):
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = ItemManager()


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = BlogManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ItemComment(models.Model):
    comment = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    objects = ItemCommentManager()
