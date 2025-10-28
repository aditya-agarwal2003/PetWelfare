from django.contrib import admin
from .models import Post, Contact, Doctor, Appointment

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


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_user_name',
        'get_doctor_name',
        'pet_name',
        'date',
        'time',
        'status',
        'created_at',
    )
    list_filter = ('status', 'date', 'doctor')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'doctor__account__first_name',
        'doctor__account__last_name',
        'pet_name',
        'reason',
    )
    ordering = ('-created_at',)
    date_hierarchy = 'date'
    list_per_page = 25

    # helper methods
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user_name.short_description = 'User'

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.account.first_name} {obj.doctor.account.last_name}"
    get_doctor_name.short_description = 'Doctor'