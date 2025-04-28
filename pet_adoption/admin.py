from django.contrib import admin
from .models import Post, Contact

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

# Register your model with the custom ModelAdmin class
admin.site.register(Contact, ContactModelAdmin)
admin.site.register(Post)
