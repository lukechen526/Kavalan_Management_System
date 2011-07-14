from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def account_manage(request):
    if request.method == 'GET':
        return render(request, 'registration/manage.html')
