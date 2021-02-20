from django.shortcuts import render
from .models import OrderItem,Order,Grocery,Transaction,Rate,Comment,Profile,Category

def index(request):
    object_list = Grocery.objects.all()
    # categories = Category.get_category()
    return render(request,'index.html',{'object_list':object_list })
