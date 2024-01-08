from django.http import HttpResponse
from django.shortcuts import render


def first_page(request):
    user = request.user
    return render(request, 'firstpage/firstpage.html', {'user': user})