from django.shortcuts import render, redirect, reverse


def index(request):
    return redirect(to=reverse('home'))


def home(request):
    return render(request, 'index.html')
