from django import forms
from .models import Post, Contact

class PetForm(forms.ModelForm):
    image = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Post
        fields = ['name', 'price', 'category', 'gender', 'image', 'post_address', 'description']

    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price:
            # Set a default value or perform additional handling if necessary
            return None
        return price


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
