from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Room, Booking, GalleryImage, HeroImage, SiteSetting, AboutCarouselImage  # <-- Added AboutCarouselImage

# --- MODEL REGISTRATIONS ---

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('room_number', 'room_type', 'price_per_night', 'is_available')
        }),
        ('Media & Details', {
            'fields': ('image', 'description'),
            'description': 'Upload a specific photo for this room and write a custom description.'
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in', 'check_out', 'total_price', 'status')
    list_filter = ('status', 'check_in')
    search_fields = ('guest_name', 'guest_email')

# --- IMAGE UPLOAD & SITE SETTINGS REGISTRATIONS ---

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

@admin.register(AboutCarouselImage)
class AboutCarouselImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')
    # You can also add a title field to this model later if you want to name them

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo')
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


# --- CUSTOM ADMIN DASHBOARD ---

admin.site.site_header = "Moonlight Hotel Administration"
admin.site.site_title = "Moonlight Admin"
admin.site.index_title = "Welcome to the Moonlight Hotel Dashboard"

original_index = admin.site.index

def custom_admin_index(request, extra_context=None):
    if extra_context is None:
        extra_context = {}
    
    # Calculate Total Revenue
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    total_revenue = sum(booking.total_price for booking in confirmed_bookings)
    
    # Calculate Total Bookings
    total_bookings_count = confirmed_bookings.count()
    
    # Add this data to the admin dashboard context
    extra_context['total_revenue'] = total_revenue
    extra_context['total_bookings_count'] = total_bookings_count
    
    return original_index(request, extra_context)

# Apply the override
admin.site.index = custom_admin_index