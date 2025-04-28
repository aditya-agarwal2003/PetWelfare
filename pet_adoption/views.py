from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, AdoptionRequest, Contact
from .constants import HEADER_TAGS, HT_SIZE
from .forms import PetForm, ContactForm
import random
from django.contrib import messages


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
