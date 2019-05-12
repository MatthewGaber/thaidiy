from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

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
    content = RichTextUploadingField(help_text="When uploading an image to the server there is no indication anything is happening but just give it a minute or so", blank=True, null=True,  # nopep8
                                         config_name='special',
                                         external_plugin_resources=[(
                                             'youtube',
                                             '/static/projects/vendor/ckeditor_plugins/youtube/youtube/',   # nopep8
                                             'plugin.js',
                                         )],
                                         )
    description = models.CharField(max_length=300,
                                   default="")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    first_image = models.CharField(max_length=400, blank=True)

    # limit content length to 30000 characters
    def clean(self):
        if len(self.content) > 30000:
            raise ValidationError(
                _('The post is to long, with the generated html it is %(value)s characters long'),  # nopep8
                params={'value': len(self.content)},
            )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    # get the first image in the editor for og tag
    def save(self, *args, **kwargs):
        img = re.search('"https://thai-diy-ninja.s3.amazonaws.com/uploads([^"]+)"', self.content)  # nopep8
        self.first_image = img.group().strip('"')
        super(Post, self).save(*args, **kwargs)


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
