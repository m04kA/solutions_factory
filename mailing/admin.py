from django.contrib import admin


from .models import *


# Register your models here.
admin.site.register(Mailings)
admin.site.register(Users)
admin.site.register(Messages)
