from django import forms
from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images import get_image_model_string
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.api import APIField

from .custom import ImageChooserBlock

from rest_framework.fields import DateField, DateTimeField
from rest_framework import serializers


@register_snippet
class Tag(index.Indexed, models.Model):
    name = models.CharField(max_length=100, null=True)

    panels = [
        FieldPanel('name')
    ]

    search_fields = [
        index.SearchField('name'),
    ]

    api_fields = [
        APIField('name'),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context



class BlogPage(Page):
    date = models.DateField("Post date")
    intro = RichTextField(blank=True)
    programming_language = models.CharField(blank=True, null=True, max_length=100)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('subtitle', blocks.CharBlock(form_classname="subtitle", required=False)),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(required=False)),
        ('quote', blocks.BlockQuoteBlock(required=False)),
        ('video', EmbedBlock(required=False)),
        ('code_snippet', blocks.TextBlock(form_classname="Code Snippet", required=False, help_text="Snippet with code"))
    ], use_json_field=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ParentalManyToManyField('Tag', blank=True)
    featured = models.BooleanField(default=False)

    def main_image(self):
        """
        Returns the image from the first gallery item or None if no gallery items exist
        """
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    api_fields = [
        APIField('date', serializer=DateField(format='%a %d %b %Y')),
        APIField('intro'),
        APIField('programming_language'),
        APIField('first_published_at', serializer=DateTimeField(format=f'%d/%m/%y')),
        APIField('latest_revision_created_at', serializer=DateTimeField(format=f'%d/%m/%y')),
        APIField('body'),
        APIField('authors', serializer=serializers.StringRelatedField(many=True)),
        APIField('tags', serializer=serializers.StringRelatedField(many=True)),
        APIField('featured'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('programming_language'),
        FieldPanel('body'),
        FieldPanel('featured'),
        InlinePanel('gallery_images', label="Gallery images")
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    caption = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    api_fields = [
        APIField('name'),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Authors'