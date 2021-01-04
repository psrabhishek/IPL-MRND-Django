from django.contrib import admin
from ipl_app import models
# Register your models here.


admin.site.register(models.Match)
admin.site.register(models.Delivery)