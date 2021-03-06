from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,OrderItem, Order, Transaction,Grocery, Category, Comment, Rate,Delivery
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignUpForm,UpdateUserProfileForm,CommentForm,RateForm,DeliveryForm, GroceryForm, UpdateGroceryForm
from .decorators import admin_only,allowed_users
from django.contrib import messages
import datetime
import requests
from django.http import JsonResponse
from decimal import *

from django.http import JsonResponse
from decimal import *


import random
from django.conf import settings
from django.views.generic.base import TemplateView



def index(request):
    object_list = Grocery.objects.all()
    categories = Category.get_category()
    return render(request,'index.html',{'object_list':object_list,'categories':categories })

def search_grocery(request):
    categories = Category.get_category()
    if 'searchproject' in request.GET and request.GET["searchproject"]:
        search_term = request.GET.get("searchproject")
        searched_project = Grocery.search_by_name(search_term)
        message = f"{search_term}"
        context = {'object_list':searched_project,'message': message,'categories':categories}
        return render(request, "search.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})  


def search_groceries(request):
    categories = Category.get_category()
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    current_order_groceries = []
    # if filtered_orders.exists():
    # 	# user_order = filtered_orders[0]
    # 	user_order_items = user_order.items.all()
    # 	current_order_groceries = [grocery.grocery for grocery in user_order_items]
    if 'searchgrocery' in request.GET and request.GET["searchgrocery"]:
        search_term = request.GET.get("searchgrocery")
        searched_project = Grocery.search_by_name(search_term)
        message = f"{search_term}"
        context = {'object_list':searched_project,'message': message,'categories':categories,'current_order_groceries': current_order_groceries,}
        return render(request, "searching.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'searching.html',{"message":message})  


def grocery_category(request, category):
    object_list = Grocery.filter_by_category(category)
    categories = Category.get_category()
    context = {'object_list':object_list,'categories': categories}
    return render(request,'category/notlogged.html',context)


# @login_required(login_url='login')
def comment(request, pk):
    image = get_object_or_404(Grocery, pk=pk)
    grocery = Grocery.objects.get(id = pk)
    rates = Rate.objects.order_by('-date')
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.grocery = image
            comment.user = request.user.profile
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    if request.method == 'POST':
        form_rate = RateForm(request.POST)
        if form_rate.is_valid():
            prices = form_rate.cleaned_data['prices']
            fresh = form_rate.cleaned_data['fresh']
            deliveries = form_rate.cleaned_data['deliveries']
            rate = Rate()
            rate.grocery = image
            rate.user = current_user
            rate.prices = prices
            rate.fresh = fresh
            rate.deliveries = deliveries
            rate.average = (rate.prices + rate.fresh + rate.deliveries)/3
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form_rate = RateForm()    
    context = {
        'image': image,
        'form': form,
        'form_rate':form_rate,
        'rates':rates,
        'grocery':grocery,
    }
    return render(request, 'grocery.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # group = Group.objects.get(name = 'customer')
            # user.groups.add(group)
            user.save()
            messages.info(request, "Your account has been Created successfully.")
            return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form}) 


def profile(request, username):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    context = {
        'prof_form': prof_form,
        'my_orders':my_orders,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def grocery_list(request):
    object_list = Grocery.objects.all()
    categories = Category.get_category()

    context = {
        'object_list': object_list,
        'categories':categories
    }
    return render(request, "groceries/grocery_list.html", context)


def groceries_category(request, category):
    object_list = Grocery.filter_by_category(category)
    categories = Category.get_category()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_groceries = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_groceries = [grocery.grocery for grocery in user_order_items]
    context = {'object_list':object_list,'categories': categories,'current_order_groceries':current_order_groceries}
    return render(request,'category/logedin.html',context)   


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, item_id):
    user_profile = get_object_or_404(Profile, user=request.user)
    grocery = Grocery.objects.filter(id=item_id).first()
    print(grocery.price)
    if 'quantity' in request.GET and request.GET["quantity"]:
        order_item = OrderItem(grocery=grocery, is_ordered=False, quantity=request.GET.get('quantity'))
        user_order = Order(owner=user_profile, is_ordered=False, )
        order_item.save()
        user_order.items=order_item
        user_order.sub_total_amount = Decimal(order_item.quantity) * Decimal(int(grocery.price))
        user_order.save()

    messages.info(request, "item added to cart")
    return redirect(reverse('grocery_list'))


@login_required(login_url='login')
def delete_from_cart(request, item_id):
    item_to_delete = Order.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('order_summary'))




@login_required(login_url='login')
def order_details(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    existing_order =Order.objects.filter(owner=user_profile, is_ordered=False)
    
    context = {
        'order': existing_order
    }
    for i in context['order']:
        print(i.items)
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required(login_url='login')
def checkout(request, **kwargs):
    client_token = 222
    current_user = request.user
    user_profile = get_object_or_404(Profile, user=request.user)
    existing_order =Order.objects.filter(owner=user_profile, is_ordered=False)
    total_amount = 0

    random_num =  random.randint(2345678909800, 9923456789000)
    public_key = settings.RAVE_PUBLIC_KEY 
    print(random_num)

    for i in existing_order:
        total_amount += i.sub_total_amount
    print(total_amount)
    publishKey = 111
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
            clear_from_cart(request)
            return redirect('grocery_list')
    else:
        form = DeliveryForm()
    context = {
        'order': existing_order,
        'client_token': client_token,
        'form':form,

        'total_amount': total_amount,
        'current_user':current_user,
        'user_profile':user_profile,
        'random_num':random_num,
        'public_key':public_key

    }
    return render(request, 'shopping_cart/checkout.html', context)


@login_required(login_url='login')
def clear_from_cart(request):
    current_user = request.user
    cat = get_object_or_404(Order, owner=current_user.id)
    cat.delete()
    messages.info(request, "Thank you for shopping with us")
    return redirect('grocery_list') 


def admin_page(request):
    if request.method == "POST":
        form = GroceryForm(request.POST,request.FILES)
        if form.is_valid():
            groceries = form.save(commit=False)
            # project.user = current_user
            groceries.save()
            return redirect('groceries')
    else:
        form = GroceryForm()
        context = {
            "form":form
        }
        return render(request, 'add_groceries.html', context)

def groceries(request):
    groc = Grocery.objects.all()
    context = {
        "groceries":groc
    }
    print(groc)
    return render(request, 'groceries.html', context)

def del_groceries(request, groc_id):
    groc = Grocery.objects.filter(id=groc_id).delete()
    context = {
        "grocery":groc
    }
    print(groc)
    return redirect('groceries')


def about (request):
    return render(request, 'about.html')

def gallery(request):
    return render(request, 'gallery.html')

def update_groceries(request, groc_id):
    groc = Grocery.objects.get(id=groc_id)
    if request.method == "POST":
        
        form = UpdateGroceryForm(request.POST,request.FILES)
        print(form.data['name'])
        if form.is_valid():
            groceries = form.save(commit=False)
            # project.user = current_user
            Grocery.objects.filter(id=groc_id).update(name=form.data['name'], description=form.data['description'], price=form.data['price'], category=form.data['category'], quantity=form.data['quantity'])
            
            return redirect('index')
    else:
        form = GroceryForm()
        context = {
            "form":form,
            "grocery": groc
        }
        return render(request, 'edit_groceries.html', context)

def orders(request):
    return render(request, 'orders.html')


def delivery(request):
    return render(request, 'delivery.html')

def order_item(request):
    return render(request, 'order_item.html')

def transaction(request):
    return render(request, 'transaction.html')


def about(request):
    return render(request,'about.html')

def deli(request):

    # client_token = 222
    # current_user = request.user
    # user_profile = get_object_or_404(Profile, user=request.user)
    # existing_order =Order.objects.filter(owner=user_profile, is_ordered=False)
    # total_amount = 0
    # for i in existing_order:
    #     total_amount += i.sub_total_amount
    # print(total_amount)
    # publishKey = 111
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
            clear_from_cart(request)
            return redirect('grocery_list')
    else:
        form = DeliveryForm()
    context = {
        # 'order': existing_order,
        # 'client_token': client_token,
        'form':form,
        # 'total_amount': total_amount
    }
    return render(request, 'deliverly.html', context)

# def payment(request):
#     return render(request,'shopping_cart/payment.php')




def contact(request):
    return render(request,'contactus.html')


def deli(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
            clear_from_cart(request)
            return redirect('grocery_list')
    else:
        form = DeliveryForm()
    context = {
        # 'order': existing_order,
        # 'client_token': client_token,
        'form':form,
        # 'total_amount': total_amount
    }
    return render(request, 'deliverly.html', context)


def transaction(request):
    transaction_items=Transaction.objects.all()
    return render(request, 'transaction.html',{"transaction":transaction_items})    


def orders(request):
    order_items=Order.objects.all()
    return render(request, 'orders.html',{"orders":order_items})    

def del_transaction(request, transaction_id):
    transaction = transaction.objects.filter(id=transaction_id).delete()
    context = {
        "transaction":transaction
    }
    print(transaction)
    return redirect('transactions')


def del_orders(request, order_id):
    order = Order.objects.filter(id=order_id).delete()
    context = {
        "order":order
    }
    print(order)
    return redirect('orders')        

class HomePageView(TemplateView):
    template_name = 'shopping_cart/checkout.html'
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['key'] = settings.RAVE_PUBLIC_KEY
    return context    

