from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
    if "admin" in request.session and request.session["admin"] == True:
        return render(request, "index.html")
    else:
        request.session.flush()
        return render(request, "fail.html")