from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    description = models.TextField(blank=True, help_text="Write a custom description for this specific room.")

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f"{self.guest_name} - Room {self.room.room_number}"
    
    @property
    def total_price(self):
        if self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            if nights > 0:
                return nights * self.room.price_per_night
        return 0

# --- MODELS FOR IMAGE UPLOADS ---

class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Gallery Image {self.id}"

class HeroImage(models.Model):
    title = models.CharField(max_length=100, blank=True, help_text="e.g., 'Luxury Suite', 'Pool View'")
    image = models.ImageField(upload_to='hero/')

    def __str__(self):
        return self.title if self.title else f"Hero Image {self.id}"

# --- SITE SETTINGS (Logo) ---

class SiteSetting(models.Model):
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload your hotel logo here.")
    site_name = models.CharField(max_length=100, default="Moonlight Hotel")
    
    # We are keeping this for a fallback, but the carousel will use the model below
    about_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload a fallback photo for the About page.")

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

# --- NEW MODEL FOR ABOUT PAGE CAROUSEL ---

class AboutCarouselImage(models.Model):
    image = models.ImageField(upload_to='about_carousel/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"About Image {self.id}"

    class Meta:
        verbose_name = "About Carousel Image"
        verbose_name_plural = "About Carousel Images"