from django.contrib import admin
from.models import Grocery,Order,OrderItem,Delivery,Category,Rate,Comment,Transaction,Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Grocery)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
admin.site.register(Category)
admin.site.register(Rate)
admin.site.register(Comment)
admin.site.register(Transaction)


