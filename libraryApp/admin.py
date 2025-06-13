from django.contrib import admin

from .models import Author
from .models import Publisher
from .models import Category
from .models import Book
from .models import BookCopy
from .models import Member
from .models import Loan

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Member)
admin.site.register(Loan)
