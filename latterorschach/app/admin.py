from django.contrib import admin

from .models import Latte, Interpretation

class InterpretationAdmin(admin.ModelAdmin):
    list_display = ( 'text' , 'user', 'latte')

admin.site.register(Latte)
admin.site.register(Interpretation, InterpretationAdmin)