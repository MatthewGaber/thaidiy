Check collectstatic

For non staff to upload image after installing djang-ckeditor naviate to -
/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/ckeditor_uploader
or equivalent and change to this 
if django.VERSION >= (1, 8):
    urlpatterns = [
        url(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
        url(r'^browse/', login_required(views.browse), name='ckeditor_browse'),
    ]

and add this

from django.contrib.auth.decorators import login_required

