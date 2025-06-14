from django.http import HttpResponse
from .models import Book
from django.template import loader

def index(request):
    all_books = Book.objects.all()
    template = loader.get_template("libraryApp/index.html")
    context = {"all_books": all_books}
    return HttpResponse(template.render(context, request))

def books(request):
    books = Book.objects.all()
    template = loader.get_template("libraryApp/books/index.html")
    context = {"books": books}
    return HttpResponse(template.render(context, request))
