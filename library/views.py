from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from cart.forms import CartAddProductForm
from .models import Book, Category, Favorite

User = get_user_model()


def book_list(request, category_slug=None):
    category = None
    author = None
    categories = Category.objects.all()
    books = Book.objects.filter(available=True)
    authors = []
    for book in books:
        authors.append(book.author)
    years = []
    for book in books.order_by('year'):
        years.append(book.year)
    print(years)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)
    # Фильтрация
    author = request.GET.get('author')
    year = request.GET.get('year')
    sort_by = request.GET.get('sort_by')

    if author:
        books = books.filter(author=author)

    if year:
        books = books.filter(year=year)

    # Сортировка
    if sort_by in ['name', 'year', 'author', 'category']:
        books = books.order_by(sort_by)
    return render(
        request,
        'library/book/list.html',
        {
            'authors': authors,
            'category': category,
            'categories': categories,
            'books': books,
            'section': 'catalog',
            'years': years,
        },
    )


@login_required
def favorite(request):
    template = 'library/book/favorite.html'
    user = request.user
    book_list = Book.objects.filter(
        following__user=user
    )
    paginator = Paginator(book_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'section': 'favorite',
    }
    return render(request, template, context)


def book_detail(request, id, slug):
    book = get_object_or_404(
        Book, id=id, slug=slug, available=True
    )
    cart_book_form = CartAddProductForm()
    following = Favorite.objects.filter(user=request.user, book=book)
    return render(
        request,
        'library/book/book.html',
        {
            'book': book,
            'cart_book_form': cart_book_form,
            'following': following,
        },
    )


@login_required
def book_follow(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    user.follower.get_or_create(
        user=user,
        book=book
    )
    return redirect('library:book_detail', book.id, book.slug)


@login_required
def book_unfollow(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    follow = Favorite.objects.filter(
        user=user,
        book=book
    )
    if follow.exists():
        follow.delete()
    return redirect('library:book_detail', book.id, book.slug)
