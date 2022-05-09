from django.contrib import admin
from . import models


admin.site.register(models.Tweets)

admin.site.register(models.User)
