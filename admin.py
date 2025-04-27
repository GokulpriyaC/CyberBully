from django.contrib import admin
from .models import  Report


from .models import UserProfile, Report

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'instaid', 'is_blocked')
    list_filter = ('is_blocked',)
    search_fields = ('user__username', 'instaid')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'reported_profile', 'reason', 'timestamp', 'blockchain_tx_hash')
    search_fields = ('user__username', 'reported_profile')
    list_filter = ('timestamp',)

admin.site.register(Report, ReportAdmin)