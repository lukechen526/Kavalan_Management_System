from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from accounts.models import CustomUserCreationForm
# Create your views here.

@login_required
def account_manage(request):
    if request.method == 'GET':
        return render(request, 'registration/manage.html')

    
@permission_required('auth.add_user')
def create_user(request):
    if request.method == 'GET':
        return render(request, 'registration/create_user.html', {'form': CustomUserCreationForm})
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.groups = form.cleaned_data['groups']
            user.save()
            
            return HttpResponseRedirect("/")
        else:
            return render(request, 'registration/create_user.html', {'form': form})
