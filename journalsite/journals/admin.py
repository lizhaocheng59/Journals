from django.contrib import admin

from .models import Journal, Entry
#
# admin.site.register(User)
# admin.site.register(EntryLog)
# admin.site.unregister(Journal)
# admin.site.unregister(Entry)
admin.site.register(Journal)
admin.site.register(Entry)
# Register your models here.
