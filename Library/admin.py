
from django.contrib import admin
from .models import Book, IssueBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'isbn',
        'quantity'
    )

    search_fields = (
        'title',
        'author',
        'category',
        'isbn'
    )

    list_filter = ('category',)


@admin.register(IssueBook)
class IssueBookAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'member',
        'issue_date',
        'return_date',
        'returned_on',
        'fine',
        'is_returned'
    )

    list_filter = (
        'is_returned',
        'issue_date',
        'return_date'
    )

    search_fields = (
        'book__title',
        'member__username',
        'member__email'
    )

    readonly_fields = (
        'issue_date',
        'fine'
    )

    list_per_page = 20
