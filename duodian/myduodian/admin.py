from django.contrib import admin

# Register your models here.

from myduodian.models import AiDuoDian

class DuoDianAdmin(admin.ModelAdmin):
    list_display = ['goodName','price','image']


admin.site.register(AiDuoDian,DuoDianAdmin)