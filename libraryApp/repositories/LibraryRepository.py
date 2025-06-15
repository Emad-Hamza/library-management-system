from ..models import Library, Author, BookCopy, Category
from .BaseRepository import BaseRepository
from django.db.models import Q


class LibraryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Library)

    def filter_by_author(self, author_id):
        author = Author.objects.get(id=author_id)
        libraries = Library.objects.filter(
            id__in=BookCopy.objects.filter(
                book__author=author
            ).values_list('library', flat=True))
        return libraries

    def filter(self, author_id=None, category_id=None):
        filter_condition = Q()
        if author_id:
            filter_condition &= Q(id__in=BookCopy.objects.filter(
                book__author__id=author_id))
        if category_id:
            filter_condition &= Q(id__in=BookCopy.objects.filter(
                book__categories__id=category_id)
            )
        libraries = Library.objects.filter(
            id__in=BookCopy.objects.filter(
                filter_condition
            ).values_list('library', flat=True))
        return libraries

    # Example: Get latest products
    # def get_latest_(self, limit=10):
    #     return self.model.objects.order_by('-created_at')[:limit]
