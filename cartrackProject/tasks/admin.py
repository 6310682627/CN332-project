from django.contrib import admin
from .models import OriginalVideo, Loop, Task

# class OriginalVideoAdmin(admin.ModelAdmin):
#     list_display = ("user", "video", "date",)
    
# class TrackingVideoAdmin(admin.ModelAdmin):
#     list_display = ("video",)

# class LoopAdmin(admin.ModelAdmin):
#     list_display = ("originalVideo", "trackingVideo",)


# admin.site.register(OriginalVideo, OriginalVideoAdmin)
# admin.site.register(TrackingVideo, TrackingVideoAdmin)
# admin.site.register(Loop, LoopAdmin)
admin.site.register(OriginalVideo)
# admin.site.register(TrackingVideo)
admin.site.register(Loop)
admin.site.register(Task)

