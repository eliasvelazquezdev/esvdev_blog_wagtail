from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from rest_framework.renderers import JSONRenderer

from blog.models import BlogPage, BlogTagIndexPage

class BlogPostAPIViewSet(PagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    model = BlogPage
    name = "posts"

class TagPostAPIViewSet(PagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    model = BlogTagIndexPage
    name = "tags"