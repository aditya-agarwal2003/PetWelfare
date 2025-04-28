from django.shortcuts import render

def index(request):
    context = {
        "title": "Welcome to PAW",
    }
    return render(request, "index.html", context)
