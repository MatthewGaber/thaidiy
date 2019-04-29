from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save

import io
from django.core.files.storage import default_storage as storage


class Shop(models.Model):
    name = models.CharField(max_length=100)
    shopcategory = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    details = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='shop_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('shop-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()
