from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from quote.models import Author, Quote


class QuoteAuthorInline(admin.StackedInline):
    model = Quote
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        QuoteAuthorInline,
    ]
    ordering = ['name', ]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'author',)
    list_filter = ('quote', 'author',)
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 6, 'cols': 100})},
    }
