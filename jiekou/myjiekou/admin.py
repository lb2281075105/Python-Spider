from django.contrib import admin

from  myjiekou.models import MyModel
# Register your models here.

class MyAdmin(admin.ModelAdmin):
    list_display = ["name","age","hobby"]

admin.site.register(MyModel,MyAdmin)
