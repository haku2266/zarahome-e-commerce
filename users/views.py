from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import CustomUserModel
import phonenumbers
from render_block import render_block_to_string
import re


def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    else:
        form = RegistrationForm()
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                del form.cleaned_data['confirm_password']
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                form.save()

                auth_user = authenticate(email=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'])
                if auth_user is not None:
                    login(request, auth_user)
                return redirect('shop:home')

        return render(request, 'register.html', context={'form': form,
                                                         'validate_errors': []})


# def flag_control(request):
#     if request.method == 'POST':
#         phone = request.POST.get('phone_number')
#         try:
#             code = phonenumbers.region_code_for_number(phonenumbers.parse(phone))
#         except:
#             code = ''
#         html = render_block_to_string('register.html', 'flag-update', context={'code': code})
#         return HttpResponse(html)
#
#     return render(request, 'register.html')


def email_validate(request):
    email = request.POST.get('email')
    errors = []
    pattern = r"[\w-]{1,20}@gmail\.com"
    if not re.match(pattern, email):
        errors.append('Enter a valid email address.')
    if CustomUserModel.objects.filter(email=email).exists():
        errors.append('User with that email is already exist')

    if email == '':
        errors = []

    html = render_block_to_string('register.html', 'email-val', context={
        'validate_errors': errors
    })

    return HttpResponse(html)


def password_validate(request):
    password = request.POST.get('password')
    errors = []
    if len(password) < 8:
        errors.append('This password is too short. It must contain at least 8 characters.')
    if password.isnumeric():
        errors.append('This password is entirely numeric.')

    if password == '':
        errors = []

    html = render_block_to_string('register.html', 'password-val', context={
        'validate_errors': errors
    })
    return HttpResponse(html)


def phone_validate(request):
    phone = request.POST.get('phone_number')
    phone = phone.replace(' ', '')
    errors = []
    try:
        z = phonenumbers.parse(phone)  # 998944009080
        if not phonenumbers.is_valid_number(z):
            errors.append('A phone number is not valid.')
    except:
        errors.append('A phone number is not valid.')
    if phone == '':
        errors = []
    html = render_block_to_string('register.html', 'phone-val', context={
        'validate_errors': errors
    })
    return HttpResponse(html)
