from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from demoapp1.forms.user_form import UserForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to home page after successful signup
            return redirect('show_books')
    else:
        form = UserForm()
    return render(request, 'demoapp1/signup_signin.html', {'form': form,
                                                       'is_signup': True})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                if user.role == 'olduser':
                    form.add_error(None, 'You must register as a new-user first. '
                                         'Please setup you password.')
                else:
                    login(request, user)
                    if user.role == 'admin':
                        return redirect('home')
                    else:
                        return redirect('show_books')
    else:
        form = AuthenticationForm()
    return render(request, 'demoapp1/signup_signin.html',
                  {'form': form, 'is_signup': False})


