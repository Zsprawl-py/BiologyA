from django.http import HttpResponse
from django.shortcuts import render
from courses.models import Team


def first_page(request):
    user = request.user
    return render(request, 'firstpage/firstpage.html', {'user': user})

def team(request):
    team = Team.objects.all()

    return render(request, 'firstpage/team.html', {'team':team})