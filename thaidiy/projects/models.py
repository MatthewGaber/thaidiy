from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField(blank=True, null=True,
                                         config_name='special',
                                         external_plugin_resources=[(
                                             'easyimage',
                                             '/static/projects/vendor/ckeditor_plugins/easyimage/',  # nopep8
                                             'plugin.js',
                                         ), (
                                             'youtube',
                                             '/static/projects/vendor/ckeditor_plugins/youtube/youtube/',   # nopep8
                                             'plugin.js',
                                         )],
                                         )

    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
