from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
import stripe
from django.urls import reverse
from .models import UserProfile
from formApp.models import Book
from userBook.models import Cart, CartItem


# Create your views here.

def base(request):
    user_name = request.session['username']
    return render(request,'user/userbase.html',{'user_name':user_name})


def listBook(request):
    user_name = request.session['username']

    books=Book.objects.all()

    paginator=Paginator(books,5)
    page_number= request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)



    return render(request,'user/userlistbook.html',{'books':books,'page':page,'user_name':user_name})


def detailView(request,book_id):
    user_name = request.session['username']

    book=Book.objects.get(id=book_id)

    return render(request,'user/userdetailview.html',{'book':book,'user_name':user_name})


def Search_Book(request):
    user_name = request.session['username']

    query = None
    books = None

    if 'q' in request.GET:

        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query))

    else:
        books = []

    context = {'books': books, 'query': query,'user_name':user_name}

    return render(request, 'user/usersearch.html', context)


def add_to_cart(request,book_id):
    book= Book.objects.get(id=book_id)

    if book.quantity > 0:

        user_profile, created = UserProfile.objects.get_or_create(username=request.user.username)
        cart, created = Cart.objects.get_or_create(user=user_profile)
        # cart,created = Cart.objects.get_or_create(user=request.user)
        cart_item,item_created = CartItem.objects.get_or_create(cart=cart,book=book)

        if not item_created:

            cart_item.quantity += 1
            cart_item.save()
    return redirect('viewcart')


def view_cart(request):
    user_name = request.session['username']

    user_profile, created = UserProfile.objects.get_or_create(username=request.user.username)
    cart, created = Cart.objects.get_or_create(user=user_profile)

    # cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_item = CartItem.objects.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    context={'cart_items': cart_items,
             'cart_item': cart_item,
             'total_price': total_price,
             'total_items': total_items ,
             'user_name':user_name }
    return render(request,'user/cart.html',context)


def increase_quantity(request,item_id):

    cart_item= CartItem.objects.get(id=item_id)

    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('viewcart')


def decrease_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('viewcart')


def remove_from_cart(request,item_id):

    try:
        cart_item= CartItem.objects.get(id=item_id)
        cart_item.delete()

    except cart_item.DoesNotExist:
        pass

    return redirect('viewcart')


def create_checkout_session(request):
    cart_items = CartItem.objects.all()

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method=='POST':
            line_items=[]
            for cart_item in cart_items:
                if cart_item.book:
                    line_item = {
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.price * 100),
                            'product_data':{
                                'name':cart_item.book.title
                            },
                        },
                        'quantity':cart_item.quantity
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = line_items,
                    mode = 'payment',
                    success_url = request.build_absolute_uri(reverse('success')),
                    cancel_url = request.build_absolute_uri(reverse('cancel'))

                )
                return redirect(checkout_session.url,code=303)



def success(request):
    user_name = request.session['username']

    cart_items = CartItem.objects.all()

    for cart_item in cart_items:
        product = cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()


    cart_items.delete()

    return render(request,'user/success.html',{'user_name':user_name})


def cancel(request):
    user_name = request.session['username']

    return render(request,'user/cancel.html',{'user_name':user_name})