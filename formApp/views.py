from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from .forms import AuthorForm,BookForm
from django.http import HttpResponse
# Create your views here.

from .models import Book,Author

def listBook(request):
    user_name=request.session['username']

    books=Book.objects.all()

    paginator=Paginator(books,5)
    page_number= request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)



    return render(request,'admin/listbook.html',{'books':books,'page':page,'user_name': user_name})

def detailView(request,book_id):
    user_name=request.session['username']

    book=Book.objects.get(id=book_id)

    return render(request,'admin/detailview.html',{'book':book,'user_name': user_name})



def updateView(request,book_id):
    user_name=request.session['username']

    book = Book.objects.get(id=book_id)

    if request.method=='POST':
        form= BookForm(request.POST,request.FILES,instance=book)

        if form.is_valid():
            form.save()

            return redirect('listbook')

    else:
        form=BookForm(instance=book)

    return render(request,'admin/updateview.html',{'form':form,'user_name': user_name})

def deleteView(request,book_id):
    user_name=request.session['username']

    book= Book.objects.get(id=book_id)

    if request.method=='POST':

        book.delete()

        return redirect('listbook')

    return render(request,'admin/deleteview.html',{'book':book,'user_name': user_name})


def Search_Book(request):
    user_name=request.session['username']

    query = None
    books = None

    if 'q' in request.GET:

        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query))

    else:
        books = []

    context = {'books': books, 'query': query,'user_name': user_name}

    return render(request, 'admin/search.html', context)


def createBook(request):
    user_name=request.session['username']

    books=Book.objects.all()

    if request.method=='POST':
        form=BookForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()

            return redirect('listbook')

    else:
        form=BookForm()

    return render(request,'admin/book.html',{'form':form,'books':books,'user_name': user_name})


def Create_Author(request):
    user_name=request.session['username']

    if request.method=='POST':

        form= AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('listbook')

    else:
        form= AuthorForm()

    return render(request,'admin/author.html',{'form':form,'user_name': user_name})


def base(request):
    user_name=request.session['username']

    return render(request,'admin/adminbase.html',{'user_name': user_name,})
