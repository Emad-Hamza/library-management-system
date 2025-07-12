from ..models import Author, Book, Category
from .BaseRepository import BaseRepository
from django.db.models import Q, F
from django.db.models import Count, Prefetch


class AuthorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Author)

    def filter(self, library_id=None, category_id=None, is_loaded=False):
        filter_condition = Q()
        if library_id:
            filter_condition &= Q(books__copies__library_id=library_id)

        if category_id:
            categories_arr = [category_id]
            filter_condition &= Q(books__categories__in=categories_arr)

        authors = Author.objects.annotate(
            books_in_library=Count(
                'books__copies',
                filter=filter_condition,
                distinct=True
            ),
        ).filter(books_in_library__gt=0)

        if (is_loaded):
            authors = authors.prefetch_related(Prefetch('books',
                                                        queryset=Book.objects.prefetch_related(
                                                            Prefetch('categories',
                                                                     queryset=Category.objects.all(),
                                                                     to_attr='book_categories', )
                                                        ).all(),
                                                        to_attr='books_list'))

        return authors

    # Example: Get latest products
    # def get_latest_(self, limit=10):
    #     return self.model.objects.order_by('-created_at')[:limit]
