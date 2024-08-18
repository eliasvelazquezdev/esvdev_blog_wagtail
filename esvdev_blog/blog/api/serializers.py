from rest_framework import serializers
from wagtail.api.v2.serializers import PageSerializer
from blog.models import BlogPage

class BlogPageSerializer(PageSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['intro'] = instance.intro
        return representation