from django.contrib import admin

from .models import Author, Library, Publisher, Category, Book, Member, Loan, BookCopy

admin.site.register(Library)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Member)
admin.site.register(Loan)
