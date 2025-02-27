from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from django.http import HttpResponse

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'bookmagazine/category_list.html', {'categories': categories})

def book_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)
    all_categories = Category.objects.all()
    return render(request, 'bookmagazine/book_list.html', {'category': category, 'books': books, 'categories': all_categories})

def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    response = HttpResponse(book.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
    return response
