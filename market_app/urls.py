from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views


urlpatterns=[
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
