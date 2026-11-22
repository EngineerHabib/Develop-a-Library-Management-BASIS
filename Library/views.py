
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Book, IssueBook
from .forms import RegisterForm, BookForm


# Admin Permission
def admin_required(view):
    return user_passes_test(
        lambda user: user.is_staff,
        login_url='dashboard'
    )(view)


# Registration
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Registration successful! Please login.'
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# Login
def login_view(request):

    if request.method == 'POST':
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username_email,
            password=password
        )

        if user is None:
            matched_user = User.objects.filter(
                email__iexact=username_email
            ).first()

            if matched_user:
                user = authenticate(
                    request,
                    username=matched_user.username,
                    password=password
                )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username/email or password!'
        )

    return render(request, 'login.html')


# Logout
@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


# Dashboard
@login_required
def dashboard(request):

    if request.user.is_staff:

        issued_books = IssueBook.objects.all()

        total_members = User.objects.filter(
            is_staff=False
        ).count()

        all_issues = IssueBook.objects.all()

    else:

        issued_books = IssueBook.objects.filter(
            member=request.user
        )

        total_members = 0

        all_issues = IssueBook.objects.filter(
            member=request.user
        )

    total_fine = sum(
        (issue.fine for issue in all_issues),
        Decimal('0.00')
    )

    context = {
        'issued_books': issued_books,
        'total_books': Book.objects.count(),
        'total_members': total_members,
        'total_issued': issued_books.filter(
            is_returned=False
        ).count(),
        'total_fine': total_fine,
    }

    return render(request, 'dashboard.html', context)


# Book Search
@login_required
def book_list(request):

    query = request.GET.get('q', '')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

    return render(
        request,
        'book_list.html',
        {
            'books': books,
            'query': query
        }
    )


# Add Book (Admin Only)
@login_required
@admin_required
def add_book(request):

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Book added successfully!'
            )

            return redirect('book_list')

    else:
        form = BookForm()

    return render(
        request,
        'book_form.html',
        {
            'form': form,
            'title': 'Add Book'
        }
    )


# Update Book (Admin Only)
@login_required
@admin_required
def update_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Book updated successfully!'
            )

            return redirect('book_list')

    else:
        form = BookForm(instance=book)

    return render(
        request,
        'book_form.html',
        {
            'form': form,
            'title': 'Update Book'
        }
    )


# Delete Book (Admin Only)
@login_required
@admin_required
def delete_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()

        messages.success(
            request,
            'Book deleted successfully!'
        )

        return redirect('book_list')

    return render(
        request,
        'book_confirm_delete.html',
        {'book': book}
    )


# Issue Book (Member Only)
@login_required
def issue_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.user.is_staff:
        messages.error(
            request,
            'Admin cannot issue books!'
        )
        return redirect('book_list')

    if request.method == 'POST':

        if book.quantity > 0:

            already_issued = IssueBook.objects.filter(
                book=book,
                member=request.user,
                is_returned=False
            ).exists()

            if already_issued:

                messages.warning(
                    request,
                    'You already issued this book!'
                )

            else:

                IssueBook.objects.create(
                    book=book,
                    member=request.user,
                    return_date=(
                        timezone.localdate() + timedelta(days=14)
                    )
                )

                book.quantity -= 1
                book.save()

                messages.success(
                    request,
                    'Book issued successfully!'
                )

        else:

            messages.error(
                request,
                'Book is not available!'
            )

    return redirect('dashboard')


# Return Book (Member Only)
@login_required
def return_book(request, pk):

    if request.user.is_staff:
        messages.error(
            request,
            'Admin cannot return books!'
        )
        return redirect('dashboard')

    issue = get_object_or_404(
        IssueBook,
        pk=pk,
        member=request.user,
        is_returned=False
    )

    if request.method == 'POST':

        today = timezone.localdate()

        issue.returned_on = today
        issue.is_returned = True

        issue.save()

        issue.book.quantity += 1
        issue.book.save()

        messages.success(
            request,
            f'Book returned successfully! Fine: Tk {issue.fine}'
        )

    return redirect('dashboard')


# All Issued Books (Admin Only)
@login_required
@admin_required
def issue_list(request):

    issues = IssueBook.objects.all()

    return render(
        request,
        'issue_list.html',
        {'issues': issues}
    )
