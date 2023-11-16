from wagtail.api.v2.router import WagtailAPIRouter
from .views import BlogPostAPIViewSet, TagPostAPIViewSet

api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('posts', BlogPostAPIViewSet)
api_router.register_endpoint('tags', TagPostAPIViewSet)