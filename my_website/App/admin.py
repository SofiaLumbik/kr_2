from django.contrib import admin
from .models import Product, HomePage, ContactPage, Order, Classmate, EducationProgram

admin.site.register(Product)
@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('banner_title', 'banner_subtitle')
    class Media:
        css = {
            'all': ('ckeditor/ckeditor.css',)
        }

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'product', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('first_name', 'last_name', 'email')

class ClassmateInline(admin.TabularInline):
    model = Classmate
    extra = 1

@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    inlines = [ClassmateInline]