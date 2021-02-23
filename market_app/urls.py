from django.urls import path, include
from .views import index,search_groceries,search_grocery, grocery_category, comment, signup, profile, grocery_list, groceries_category, get_user_pending_order,add_to_cart, delete_from_cart, order_details, checkout, clear_from_cart, admin_page, about, groceries, del_groceries, update_groceries,orders,order_item,comment,delivery,transaction
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views


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
    path('add/groceries', admin_page, name='add_groceries'),
    path('groceries', groceries, name='groceries'),
    path('delete/groceries/<groc_id>', del_groceries, name='del_groceries'),
    path('update/groceries/<groc_id>', update_groceries, name='update_groceries'),
    path('orders/',orders,name = 'orders'),
    path('comment/',comment,name = 'comment'),
    path('delivery/',delivery,name = 'delivery'),
    path('transaction/',transaction,name = 'transaction'),
    path('order_item/',order_item,name = 'order_item'),




] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    path('',views.index,name = 'index'),
    path('category/<category>',views.grocery_category,name = 'category'),
    path('categories/<category>',views.groceries_category,name = 'categories'),
    path('grocery_list/',views.grocery_list,name = 'grocery_list'),
    path('signup/',views.signup , name='signup'),
    path('grocery/<pk>', views.comment, name='comment'),
    path('profile/<username>/', views.profile, name='profile'),
    path('clear_from_cart/',views.clear_from_cart,name='clear_from_cart'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('search',views.search_grocery,name = 'search_grocery'),
    path('searching',views.search_groceries,name = 'search_groceries'),
    path('about/',views.about,name = 'about'),
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', views.order_details, name="order_summary"),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
    url(r'^checkout/$', views.checkout, name='checkout'),
]
