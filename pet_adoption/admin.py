from django.contrib import admin
from .models import Post, Contact, Doctor

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

# Register your model with the custom ModelAdmin class
admin.site.register(Contact, ContactModelAdmin)
admin.site.register(Post)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('account', 'specialization', 'clinic_name', 'pincode', 'account__phone_number')
    search_fields = ('account__first_name', 'account__last_name', 'clinic_name', 'pincode', 'specialization', 'account__phone_number')
    list_filter = ('pincode', 'specialization')