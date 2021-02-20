from django.urls import path, include
from .views import index,search_groceries,search_grocery, grocery_category, comment, signup, profile, grocery_list, groceries_category, get_user_pending_order,add_to_cart, delete_from_cart, order_details, checkout, clear_from_cart, admin_page, about
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    path('',index,name = 'index'),
    path('category/<category>',grocery_category,name = 'category'),
    path('categories/<category>',groceries_category,name = 'categores'),
    path('grocery_list/',grocery_list,name = 'grocery_list'),
    path('signup/',signup , name='signup'),
    path('grocery/<pk>', comment, name='comment'),
    path('profile/<username>/', profile, name='profile'),
    path('clear_from_cart/',clear_from_cart,name='clear_from_cart'),
    path('admin_page',admin_page,name='admin_page'),
    path('search',search_grocery,name = 'search_grocery'),
    path('searching',search_groceries,name = 'search_groceries'),
    path('about/',about,name = 'about'),
    path('add-to-cart/<item_id>/', add_to_cart, name="add_to_cart"),
    path('order-summary/', order_details, name="order_summary"),
    path('item/delete/<item_id>', delete_from_cart, name='delete_item'),
    path('checkout/', checkout, name='checkout'),


] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)