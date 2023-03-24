from django.contrib import admin
from .models import OriginalVideo, TrackingVideo

class OriginalVideoAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "date",)
    
class TrackingVideoAdmin(admin.ModelAdmin):
    list_display = ("video",)

admin.site.register(OriginalVideo, OriginalVideoAdmin)
admin.site.register(TrackingVideo, TrackingVideoAdmin)