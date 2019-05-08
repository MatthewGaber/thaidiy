from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
from django.core.files.storage import default_storage as storage
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def clean(self):
        if self.image.width > 3000 or self.image.height > 3000:
            raise ValidationError(
                _('Max width and height is 3000 pixels, width = %(value)s and height = %(hvalue)s '),  # nopep8
                params={'value': self.image.width, 'hvalue': self.image.height},  # nopep8
            )

    def __str__(self):
        return f'{self.user.username} Profile'

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
