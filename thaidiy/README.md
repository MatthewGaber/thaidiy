The app has been deployed at https://thaidiyninja.herokuapp.com

The app will only run on localhost with debug:true

AWS S3 is used for image storage with signed URL's

There are 3 apps
users
shops
projects

The projects/Post model uses the django-ckeditor library for the wysiwyg editor, it has been customised and the project uses the repo at MatthewGaber.django-ckeditor as per requirements.txt

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

This tutorial was used for the CBV's and User App- https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

Pillow has been used to resize any uploaded images, specifically user profile, Shop and any images uploaded in the CKEditor.

An email confirmation is sent upon registration, uses built in TokenGenerator

Password can be reset via email
