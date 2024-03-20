from django.urls import path,re_path
from ecommerceapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('checkout/',views.checkout,name="checkout"),
    path('handlerequest/',views.handlerequest,name="HandleRequest"),
    path('profile/',views.profile,name="profile"),
    # path('orderplaced/',views.orderplaced,name="orderplaced"),

    # re_path(r'(?P<id>\d+)/share/$',views.mail_send_view),

    

    
]
# / == " " #slash is nothing but it is empty space