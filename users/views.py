from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
import phonenumbers
from render_block import render_block_to_string


def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        print('got posted')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print('got valid')
            del form.cleaned_data['confirm_password']
            form.save()

            return redirect('users:register')
    return render(request, 'register.html', context={'form': form})


def flag_control(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        try:
            code = phonenumbers.region_code_for_number(phonenumbers.parse(phone))
        except:
            code = ''
        html = render_block_to_string('register.html', 'flag-update', context={'code': code})
        return HttpResponse(html)

    return render(request, 'register.html')
