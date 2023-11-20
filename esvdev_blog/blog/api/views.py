from wagtail.api.v2.views import PagesAPIViewSet, BaseAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from rest_framework.renderers import JSONRenderer


from blog.models import BlogPage, Tag

class BlogPostAPIViewSet(PagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    model = BlogPage
    name = "posts"
    
    def get_queryset(self):
        return self.model.objects.live().order_by('-first_published_at')

class TagPostAPIViewSet(BaseAPIViewSet):
    renderer_classes = [JSONRenderer]
    model = Tag
    name = "tags"

    body_fields = BaseAPIViewSet.body_fields + [
        'name',
    ]

    listing_default_fields = BaseAPIViewSet.listing_default_fields + [
        'name',
    ]





class PostImagesAPIViewSet(ImagesAPIViewSet):
    renderer_classes = [JSONRenderer]
    name = "images"