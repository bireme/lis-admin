from django.contrib import admin
from models import *

class GenericAdmin(admin.ModelAdmin):
    exclude = ('created', 'creator', 'updated', 'updater')

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'updater') and hasattr(obj, 'creator'):
            if change:
                obj.updater = request.user
            else:
                obj.creator = request.user
                obj.updater = request.user
        obj.save()    



class LanguageLocalAdmin(admin.TabularInline):
    model = LanguageLocal
    extra = 0

class LanguageAdmin(GenericAdmin):
    model = Language
    inlines = [LanguageLocalAdmin,]


admin.site.register(Language, LanguageAdmin)