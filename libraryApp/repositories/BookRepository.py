from ..models import Library, Author, BookCopy, Category, Book
from .BaseRepository import BaseRepository
from django.db.models import Q


class BookRepository(BaseRepository):
    def __init__(self):
        super().__init__(Book)

    def filter(self, author_id=None, category_id=None, library_id=None):
        filter_condition = Q()
        if author_id:
            filter_condition &= Q(author__id=author_id)
        if category_id:
            categories_arr = [category_id]
            filter_condition &= Q(categories__in=categories_arr)
        if library_id:
            filter_condition &= Q(copies__library_id=library_id)

        books = Book.objects.filter(
            filter_condition
        ).distinct()
        return books

    # Example: Get latest products
    # def get_latest_(self, limit=10):
    #     return self.model.objects.order_by('-created_at')[:limit]
