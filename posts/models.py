from django.db import models

from posts.choices import LanguageChoices
from posts.validators import BadWordValidator


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(validators=[BadWordValidator(bad_words=['bad', 'ugly', 'stupid'])])
    author = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    language = models.CharField(max_length=20, choices=LanguageChoices.choices, default=LanguageChoices.PYTHON)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('approve_post', 'Can approve post')
        ]

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)



    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'

