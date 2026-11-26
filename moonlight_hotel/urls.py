from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bookings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- NEW PAGES ---
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('services/', views.services, name='services'),
    path('location/', views.location, name='location'),
    
    # --- BOOKING SYSTEM (Moved to /rooms/) ---
    path('rooms/', views.room_list, name='room_list'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    
    # --- AUTHENTICATION ---
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')), 

    # --- USER PROFILE ---
    path('profile/', views.profile, name='profile'),
]

# --- SERVE MEDIA FILES DURING DEVELOPMENT ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)