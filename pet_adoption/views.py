from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, AdoptionRequest, Contact, Doctor, Appointment, Prescription
from .constants import HEADER_TAGS, HT_SIZE
from .forms import PetForm, ContactForm, PrescriptionForm
import random
from django.contrib import messages
from django.utils import timezone
from django.http import Http404


# Create your views here.

def landing_page(request):
    data = {}
    data['posts'] = Post.objects.filter(is_active=True).order_by(
        '-created_at'
    )
    return render(request, 'pet_adoption/landing.html', data)


def about(request):

    return render(request, 'pet_adoption/about.html')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            phone_number = contact_form.cleaned_data['phone_number']
            email = contact_form.cleaned_data['email']
            subject = contact_form.cleaned_data['subject']
            message = contact_form.cleaned_data['message']
            contact = Contact.objects.create(
                name=name, phone_number=phone_number, email=email,
                subject=subject, message=message
            )
            contact.save()
            messages.success(request, 'Your message has been recorded. We will get back to you soon!.')
            return redirect('contact')
    else:
        contact_form = ContactForm()
        data = {
            'contact_form': contact_form,
        }
        return render(request,'pet_adoption/contact.html', data)

    


@login_required
def create_post(request):
    user = request.user
    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES, instance=user)
        if pet_form.is_valid():
            name = pet_form.cleaned_data['name']
            price = pet_form.cleaned_data['price']
            category = pet_form.cleaned_data['category']
            gender = pet_form.cleaned_data['gender']
            image = pet_form.cleaned_data['image']
            post_address = pet_form.cleaned_data['post_address']
            description = pet_form.cleaned_data['description']
            post = Post.objects.create(user=user, name=name, price=price, category=category,
                                       gender=gender, image=image, post_address=post_address,
                                       description=description)
            post.save()
            messages.success(request, 'Your Post has been create successfully!.')
            return redirect(reverse('see_details', kwargs={'post_id': post.id}))
    else:
        pet_form = PetForm(instance=user)
        data = {
            'pet_form': pet_form,
            'user': user
        }

        return render(request,'pet_adoption/create_post.html', data)


def see_details(request, post_id):
    data = {}
    rand_ind = random.randint(0, HT_SIZE)
    post = Post.objects.get(id=post_id, is_active=True)
    data['related'] = Post.objects.filter(
        category=post.category, is_active=True
    ).exclude(id=post_id).order_by('-created_at')[:4]
    data['post'] = post
    data['header_tag'] = HEADER_TAGS[rand_ind]
    data['requests'] = AdoptionRequest.objects.filter(
        post=post, is_active=True
    )
    print(data)
    try:
        data['is_requested'] = AdoptionRequest.objects.get(
            user=request.user, post=post, is_active=True
        )
    except Exception:
        data['is_requested'] = None
    return render(request, 'pet_adoption/see_details.html', data)


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    AdoptionRequest.objects.filter(
        post=post
    ).delete()
    post.delete()
    return redirect('landing_page')


@login_required
def make_adopt_request(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    AdoptionRequest.objects.get_or_create(
        user=user, post=post, is_active=True
    )
    messages.success(request, 'Requested for Adoption!')
    return redirect(reverse('see_details', kwargs={'post_id': post.id}))


@login_required
def delete_adopt_request(request, ad_id):
    try:
        ad_obj = AdoptionRequest.objects.get(id=ad_id)
        post_id = ad_obj.post.id
        ad_obj.delete()
        messages.success(request, 'Successfully Deleted Request!')
    except Exception:
        messages.error(request, 'Failed Deleting Request!')
    return redirect(reverse('see_details', kwargs={'post_id': post_id}))


@login_required(login_url='login')
def find_doctor(request):
    query = request.GET.get('q', '')
    pincode = request.GET.get('pincode', '')

    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(
            Q(account__first_name__icontains=query) |
            Q(account__last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(clinic_name__icontains=query)
        )

    if pincode:
        doctors = doctors.filter(pincode__icontains=pincode)

    context = {
        'doctors': doctors,
        'query': query,
        'pincode': pincode,
    }
    return render(request, 'pet_adoption/find_doctor.html', context)


@login_required(login_url='login')
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        reason = request.POST.get('reason')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Basic validation
        if not (pet_name and reason and date and time):
            messages.error(request, "All fields are required.")
        else:
            Appointment.objects.create(
                user=request.user,
                doctor=doctor,
                pet_name=pet_name,
                reason=reason,
                date=date,
                time=time,
                status='pending',
                created_at=timezone.now()
            )
            messages.success(request, "Appointment booked successfully!")
            return redirect('my_appointments')

    context = {
        'doctor': doctor,
    }
    return render(request, 'pet_adoption/book_appointment.html', context)


@login_required(login_url='login')
def my_appointments(request):
    """Show all appointments of the logged-in user."""
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pet_adoption/my_appointments.html', {'appointments': appointments})


@login_required(login_url='login')
def cancel_appointment(request, appointment_id):
    """Cancel an appointment if it's still pending or confirmed."""
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, f"Appointment with Dr. {appointment.doctor.account.first_name} has been cancelled.")
    else:
        messages.warning(request, "This appointment cannot be cancelled.")

    return redirect('my_appointments')


@login_required(login_url='login')
def cancel_appointment_doctor(request, appointment_id):
    """Cancel an appointment if it's still pending or confirmed."""
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor__account=request.user)

    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, f"Appointment has been cancelled.")
    else:
        messages.warning(request, "This appointment cannot be cancelled.")

    return redirect('dashboard')


@login_required
def confirm_appointment(request, appointment_id):
    # Ensure the logged-in user is a doctor
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Access denied. Doctors only.")
        return redirect('dashboard')  # redirect to normal user dashboard

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)

    if appointment.status != 'pending':
        messages.warning(request, "This appointment has already been processed.")
        return redirect('dashboard')

    appointment.status = 'confirmed'
    appointment.save()
    messages.success(request, f"Appointment #{appointment.id} confirmed successfully!")
    return redirect('dashboard')


@login_required
def complete_appointment(request, appointment_id):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    appointment.status = 'completed'
    appointment.save()
    messages.success(request, f"Appointment #{appointment.id} marked as completed.")
    return redirect('dashboard')


@login_required
def add_prescription(request, appointment_id):
    # Ensure only doctors can access this page
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Only doctors can add prescriptions.")
        return redirect('dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)

    # Allow prescriptions only for confirmed appointments
    if appointment.status != 'confirmed':
        messages.warning(request, "Prescription can only be added for confirmed appointments.")
        return redirect('dashboard')

    # Create or fetch an existing prescription for this appointment
    prescription, created = Prescription.objects.get_or_create(appointment=appointment)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            messages.success(request, "Prescription saved successfully!")
            return redirect('dashboard')
    else:
        form = PrescriptionForm(instance=prescription)

    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'pet_adoption/add_prescription.html', context)


@login_required
def view_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure that only the doctor or the patient can view this prescription
    if request.user != appointment.user and (
        not hasattr(request.user, 'doctor') or request.user.doctor != appointment.doctor
    ):
        raise Http404("You are not authorized to view this prescription.")

    # Make sure the appointment actually has a prescription
    if not hasattr(appointment, 'prescription'):
        messages.warning(request, "No prescription found for this appointment.")
        return redirect('dashboard')

    prescription = appointment.prescription

    context = {
        'appointment': appointment,
        'prescription': prescription,
    }
    return render(request, 'pet_adoption/view_prescription.html', context)