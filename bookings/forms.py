from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Room, Booking  # <-- Added so BookingForm knows about Room and Booking

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # This automatically adds the Tailwind styling to all fields
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-blue-900 outline-none transition bg-gray-50'


class BookingForm(forms.ModelForm):
    # Filters the dropdown to only show available rooms
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_available=True))

    class Meta:
        model = Booking
        # Notice: guest_name and guest_email are removed from the fields list
        fields = ['room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    # Date Validation Logic
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_out <= check_in:
                raise ValidationError("Check-out date must be after the check-in date.")
        
        return cleaned_data