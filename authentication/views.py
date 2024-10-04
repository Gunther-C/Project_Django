from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.edit import FormView

from .forms import Registration, Connection, NewPassword, NewEmail


def registration(request):

    if request.method == 'POST':
        form = Registration(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.add_message(request, messages.WARNING, f"{error}")
            form.errors.clear()

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


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = NewPassword
    template_name = 'change_password.html'
    success_url = reverse_lazy('auth:login')
    success_message = "Votre mot de passe est modifié"

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.add_message(self.request, messages.WARNING, f"{error}")
        form.errors.clear()
        return super().form_invalid(form)


class UserEmailChangeView(SuccessMessageMixin, LoginRequiredMixin, FormView):
    form_class = NewEmail
    template_name = 'change_mail.html'
    success_url = reverse_lazy('auth:login')
    success_message = "Votre adresse e-mail est modifiée"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        new_email = form.cleaned_data.get('new_mail1')
        self.request.user.email = new_email
        self.request.user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.add_message(self.request, messages.WARNING, f"{error}")
        form.errors.clear()
        return super().form_invalid(form)
