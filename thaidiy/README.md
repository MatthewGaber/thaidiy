

In the django-ckeditor at MatthewGaber.django-ckeditor the following has been changed

ckeditor_uploader/urls.py 
if django.VERSION >= (1, 8):
    urlpatterns = [
        url(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
        url(r'^browse/', login_required(views.browse), name='ckeditor_browse'),
    ]

ckeditor_uploader/views.py
def post(self, request, **kwargs):
    if uploaded_file.size > 30000000:


ckeditor_uploader/backends/pillowbackend.py
def save_as(self, filepath):
    for orientation in ExifTags.TAGS.keys():

    imager = imager.resize((basewidth,hsize), Image.ANTIALIAS).convert('RGB')

Post limits
def clean(self):
        if len(self.content) > 30000: