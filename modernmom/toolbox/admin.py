from django.contrib import admin
from models import *

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

admin.site.register(Download)
admin.site.register(Image)


    

