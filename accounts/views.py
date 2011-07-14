from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def account_manage(request):
    if request.method == 'GET':
        return render(request, 'registration/manage.html')

    
@permission_required('auth.add_user')
def create_user(request):
    if request.method == 'GET':
        return render(request, 'registration/create_user.html', {'form': UserCreationForm})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.cleaned_data['password1'] == form.cleaned_data['password2']:
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            return HttpResponseRedirect("/")
        else:
            return render(request, 'registration/create_user.html', {'form': form})
