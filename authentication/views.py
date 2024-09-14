from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import Registration, Connection


def registration(request):

    if request.method == 'POST':
        form = Registration(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

        else:
            error_messages = '\n'
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages += f"{error} \n"
            form.errors.clear()
            messages.add_message(request, messages.WARNING, error_messages)

    else:
        form = Registration()

    return render(request, 'registration.html', {'form': form})


def connection(request):

    logout(request)
    text_message = ' '

    if request.method == 'POST':
        form = Connection(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Vous êtes connecté.')
                return redirect('/env/user_flux/')

            else:
                text_message = 'E-mail ou Mot de passe invalide.'

    else:
        form = Connection()

    messages.add_message(request, messages.WARNING, text_message)

    return render(request, 'login.html', {'form': form})
