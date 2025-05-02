from django.shortcuts import render, redirect
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    if request.method == "POST":
        # Handle appointment form submission
        name = request.POST['name']
        email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']
        message = request.POST.get('message', '')

        # Save the appointment in the database
        appointment = Appointment(name=name, email=email, date=date, time=time, message=message)
        appointment.save()

        # Send email to the clinic and the patient
        send_mail(
            f"New Appointment Request from {name}",
            f"Appointment details:\nName: {name}\nEmail: {email}\nDate: {date}\nTime: {time}\nMessage: {message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CLINIC_EMAIL],
        )

        send_mail(
            "Appointment Request Confirmation",
            f"Dear {name},\n\nYour appointment has been successfully booked for {date} at {time}. We will contact you if further details are needed.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return redirect('home')  # Redirect to home page after submitting

    return render(request, 'appointments/home.html')

def about(request):
    return render(request, 'appointments/about.html')

def contact(request):
    return render(request, 'appointments/contact.html')
