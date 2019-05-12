from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image, ExifTags
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import io
from django.core.files.storage import default_storage as storage

CATEGORIES = (
    ("General", "General"),
    ("Home DIY", "Home DIY"),
    ("Electronics", "Electronics"),
    ("Schools", "Schools"),
    ("Restaraunts", "Restaraunts"),
    ("Noodles", "Noodles"),
)


class Shop(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    description = models.CharField(max_length=200)
    details = models.TextField(max_length=10000)
    image = models.ImageField(default='default.jpg', upload_to='shop_pics')  # nopep8
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True)  # nopep8
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True)  # nopep8
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.image.width > 3000 or self.image.height > 3000:
            raise ValidationError(
                _('Max width and height is 3000 pixels, width = %(value)s and height = %(hvalue)s '),  # nopep8
                params={'value': self.image.width, 'hvalue': self.image.height},  # nopep8
            )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('shop-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 600 or img.width > 600:
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

            basewidth = 600
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            in_mem_file = io.BytesIO()
            if self.image.name.endswith('.jpg'):
                img.save(in_mem_file, format='JPEG')
            else:
                img.save(in_mem_file, format='PNG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()


class Comment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='comments')  # nopep8
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_comment_author')  # nopep8
    text = models.TextField(max_length=2048, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text