from rest_framework.pagination import PageNumberPagination

class BlogPostsPagination(PageNumberPagination):
    page_size = 2
