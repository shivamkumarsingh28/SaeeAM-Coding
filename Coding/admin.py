from django.contrib import admin
from .models import *


admin.site.register(Post)

admin.site.register(Category)

admin.site.site_header = 'SaeeAM ADMIN'