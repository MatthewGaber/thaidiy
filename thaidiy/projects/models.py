from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save

# todo add category models
CATEGORIES = (
    ("General", "General"),
    ("Home DIY", "Home DIY"),
    ("Electronics", "Electronics"),
    ("Schools", "Schools"),
    ("Visas", "Visas"),
    ("Restaraunts", "Restaraunts"),
    ("Noodles", "Noodles"),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES, default=CATEGORIES[0])  # nopep8
    content = RichTextUploadingField(blank=True, null=True,
                                         config_name='special',
                                         external_plugin_resources=[(
                                             'youtube',
                                             '/static/projects/vendor/ckeditor_plugins/youtube/youtube/',   # nopep8
                                             'plugin.js',
                                         )],
                                         )
    description = models.CharField(max_length=200,
                                   default="A description of the project")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # nopep8
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2048, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
