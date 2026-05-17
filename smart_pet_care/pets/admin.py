from django.contrib import admin
from .models import Pet, Adoption, Reminder, ChatbotQuery, UserProfile

# ============================================
# PET ADMIN
# ============================================

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'pet_type', 'age', 'status', 'added_date']
    list_filter = ['pet_type', 'status', 'added_date']
    search_fields = ['name', 'breed', 'description']
    list_editable = ['status']
    ordering = ['-added_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'breed', 'pet_type', 'age')
        }),
        ('Details', {
            'fields': ('description', 'health_status', 'image')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


# ============================================
# ADOPTION ADMIN
# ============================================

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'pet', 'request_date', 'status', 'approved_date']
    list_filter = ['status', 'request_date']
    search_fields = ['user__username', 'pet__name']
    list_editable = ['status']
    ordering = ['-request_date']
    readonly_fields = ['request_date']


# ============================================
# REMINDER ADMIN
# ============================================

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'pet', 'reminder_type', 'reminder_date', 'reminder_time', 'is_completed']
    list_filter = ['reminder_type', 'is_completed', 'is_recurring', 'reminder_date']
    search_fields = ['title', 'user__username', 'pet__name']
    list_editable = ['is_completed']
    ordering = ['reminder_date', 'reminder_time']
    
    fieldsets = (
        ('Reminder Information', {
            'fields': ('user', 'pet', 'title', 'description', 'reminder_type')
        }),
        ('Schedule', {
            'fields': ('reminder_date', 'reminder_time', 'is_recurring')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
    )


# ============================================
# CHATBOT QUERY ADMIN
# ============================================

@admin.register(ChatbotQuery)
class ChatbotQueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_preview', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['query', 'response', 'user__username']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    def query_preview(self, obj):
        return obj.query[:50] + '...' if len(obj.query) > 50 else obj.query
    query_preview.short_description = 'Query'
    
    fieldsets = (
        ('Chat Information', {
            'fields': ('user', 'session_id')
        }),
        ('Conversation', {
            'fields': ('query', 'response')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )


# ============================================
# USER PROFILE ADMIN
# ============================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'created_at']
    list_filter = ['state', 'created_at']
    search_fields = ['user__username', 'phone', 'city', 'state']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'city', 'state', 'pincode')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
    )