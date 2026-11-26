from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking, GalleryImage, HeroImage, SiteSetting, AboutCarouselImage  # <-- Added AboutCarouselImage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, BookingForm 
from django.contrib.auth import login
from django.core.mail import send_mail

# --- NEW PUBLIC PAGES ---

def home(request):
    featured_rooms = Room.objects.all()[:3] 
    hero_images = HeroImage.objects.all()
    
    return render(request, 'bookings/home.html', {
        'featured_rooms': featured_rooms,
        'hero_images': hero_images
    })

def about(request):
    # Fetch ALL hero images for the top banner
    hero_images = HeroImage.objects.all()
    # Fetch the specific images for the side carousel
    about_carousel_images = AboutCarouselImage.objects.all()
    
    return render(request, 'bookings/about.html', {
        'hero_images': hero_images,
        'about_carousel_images': about_carousel_images  # <-- Passed to template
    })

def gallery(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'bookings/gallery.html', {'images': images})

def services(request):
    return render(request, 'bookings/services.html')

def location(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        
        subject = f"New Contact Form Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}"
        
        send_mail(
            subject,
            message_body,
            'noreply@moonlighthotel.com', 
            ['admin@moonlighthotel.com'], 
            fail_silently=False,
        )
        
        messages.success(request, "Thank you! Your message has been sent successfully.")
        return redirect('location')
        
    return render(request, 'bookings/location.html')


# --- BOOKING SYSTEM ---

@login_required
def room_list(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.filter(user=request.user, status='confirmed').order_by('-created_at')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user 
            booking.guest_name = request.user.username
            booking.guest_email = request.user.email
            
            room = booking.room
            room.is_available = False
            room.save()
            
            booking.save()
            
            subject = f"Booking Confirmation - Moonlight Hotel (Room {room.room_number})"
            message = f"""
Hello {booking.guest_name},

Thank you for booking with Moonlight Hotel!

Here are your reservation details:
----------------------------------------
Room: {room.room_number} ({room.get_room_type_display()})
Check-in: {booking.check_in}
Check-out: {booking.check_out}
Total Price: Ksh {booking.total_price}
----------------------------------------

We look forward to hosting you!

Best regards,
The Moonlight Hotel Team
"""
            send_mail(
                subject,
                message,
                'noreply@moonlighthotel.com', 
                [booking.guest_email],        
                fail_silently=False,
            )
            
            messages.success(request, f"Success! {booking.guest_name}, your booking for Room {room.room_number} is confirmed. A receipt has been sent to your email.")
            return redirect('room_list') 
    else:
        form = BookingForm()

    return render(request, 'bookings/room_list.html', {'rooms': rooms, 'form': form, 'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    room = booking.room
    
    room.is_available = True
    room.save()
    
    booking.status = 'cancelled'
    booking.save()
    
    messages.success(request, f"Booking for {booking.guest_name} has been cancelled.")
    return redirect('room_list')

# --- AUTHENTICATION ---

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Account created successfully! Welcome to Moonlight Hotel.")
            return redirect('room_list')
    else:
        form = UserRegisterForm()
    return render(request, 'bookings/register.html', {'form': form})

# --- USER DASHBOARD & DETAILS ---

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'bookings/room_detail.html', {'room': room})

@login_required
def profile(request):
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/profile.html', {'bookings': all_bookings})