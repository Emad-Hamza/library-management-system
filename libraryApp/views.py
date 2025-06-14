from django.http import HttpResponse
from .models import Book, Library, Category, Author
from django.template import loader
from pprint import pprint
from .repositories.LibraryRepository import LibraryRepository


def index(request):
    all_books = Book.objects.all()
    template = loader.get_template("libraryApp/index.html")
    context = {"books": all_books}
    return HttpResponse(template.render(context, request))


def libraries(request):
    author_id = request.GET.get('author')
    category_id = request.GET.get('category')
    library_repository = LibraryRepository()
    if author_id or category_id:
        all_libraries = library_repository.filter_by_author(author_id)
    else:
        all_libraries = Library.objects.all()

    all_authors = Author.objects.all()
    all_categories = Category.objects.all()
    template = loader.get_template("libraryApp/libraries/index.html")
    context = {"libraries": all_libraries, "authors": all_authors, "categories": all_categories}
    return HttpResponse(template.render(context, request))


def authors(request):
    all_authors = Author.objects.all()
    template = loader.get_template("libraryApp/authors/index.html")
    context = {"authors": all_authors}
    return HttpResponse(template.render(context, request))


def books(request):
    all_books = Book.objects.all()
    template = loader.get_template("libraryApp/books/index.html")
    context = {"books": all_books}
    return HttpResponse(template.render(context, request))


def categories(request):
    all_books = Category.objects.all()
    template = loader.get_template("libraryApp/categories/index.html")
    context = {"books": all_books}
    return HttpResponse(template.render(context, request))
