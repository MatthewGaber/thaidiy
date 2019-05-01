from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image, ExifTags
from django.dispatch import receiver
from django.db.models.signals import post_save

import io
from django.core.files.storage import default_storage as storage

CATEGORIES = (
    ("Home", "Home"),
    ("Electronics", "Electronics"),
    ("Schools", "Schools"),
    ("Noodles", "Noodles"),
)


class Shop(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    description = models.CharField(max_length=200)
    details = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='shop_pics')
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True)  # nopep8
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True)  # nopep8
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('shop-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(img._getexif().items())

                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
                
            except (AttributeError, KeyError, IndexError):
                pass

            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()
