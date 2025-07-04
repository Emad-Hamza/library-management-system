from ..models import Library, Author, BookCopy, Category, Book
from .BaseRepository import BaseRepository
from django.db.models import Q, F
from django.db.models import Count
from django.db.models.functions import Coalesce
from django.db.models import FilteredRelation


class AuthorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Author)

    def filter(self, library_id=None, category_id=None):
        filter_condition = Q()
        if library_id:
            filter_condition &= Q(books__copies__library_id=library_id)

        if category_id:
            categories_arr = [category_id]
            # filter_condition &= Q(id__in=Book.objects.filter(categories__in=categories_arr))
            filter_condition &= Q(books__categories__in=categories_arr)


        # projects = Project.objects.annotate(
        #     active_tasks=FilteredRelation('task', condition=Q(task__is_active=True))
        # ).filter(task__is_active=True)

        # authors = Author.objects.filter(
        #     books__copies__library_id=library_id
        # ).distinct()

        authors = Author.objects.annotate(
            books_in_library=Count(
                'books__copies',
                filter=filter_condition,
                distinct=True
            )
        ).filter(books_in_library__gt=0)

        # authors = Author.objects.all()
        return authors

    # Example: Get latest products
    # def get_latest_(self, limit=10):
    #     return self.model.objects.order_by('-created_at')[:limit]
