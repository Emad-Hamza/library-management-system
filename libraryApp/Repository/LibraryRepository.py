from ..models import Library, Author, BookCopy
from . import BaseRepository


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

    # Example: Get latest products
    def get_latest_(self, limit=10):
        return self.model.objects.order_by('-created_at')[:limit]
