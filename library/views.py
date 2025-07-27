from django.shortcuts import get_object_or_404, render
from .models import Book, Category


def book_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    books = Book.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)
    return render(
        request,
        'library/book/list.html',
        {
            'category': category,
            'categories': categories,
            'books': books,
        },
    )


def book_detail(request, id, slug):
    book = get_object_or_404(
        Book, id=id, slug=slug, available=True
    )
    return render(
        request,
        'shop/product/detail.html',
        {'book': book},
    )
