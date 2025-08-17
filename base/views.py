from django.shortcuts import render

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Kurs 1'},
    {'id': 2, 'name': 'Kurs 2'},
    {'id': 3, 'name': 'Kurs 3'},
    {'id': 4, 'name': 'Kurs 4'},
]

def home(request):
    context= {'rooms': rooms}
    return render(request, 'base/home.html' , context)

def room(request):
    return render(request,'room.html')
