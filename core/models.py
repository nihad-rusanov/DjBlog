from django.db import models
from django.contrib.auth.models import User
# Create your models here.'

class Category(models.Model):
    category_name=models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

class Blog(models.Model):
    title = models.CharField(max_length=30,blank=False)
    content = models.TextField(blank=False)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,blank=False)
    author = models.TextField(blank=False)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog,related_name='comments',on_delete=models.CASCADE,)
    author = models.ForeignKey(User,related_name='user_comments',on_delete=models.CASCADE,)
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True,blank=False)

    def __str__(self):
        return self.content


class Like(models.Model):
    blog = models.ForeignKey(Blog,related_name='likes',on_delete=models.CASCADE,)
    session_key = models.CharField(max_length=40, blank=True, null=True)

