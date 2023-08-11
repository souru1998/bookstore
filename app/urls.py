from django.contrib import admin
from django.urls import path,include
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index),
    path('login/',views.login),
    path('noload/',views.noload),
    path('about/',views.about),
    path('address/',views.address),
    path('alerts/',views.alerts),
    path('base/',views.base),
    path('blogfullwidth/',views.blogfullwidth),
    path('bloggrid/',views.bloggrid),
    path('blogleftsidebar/',views.blogleftsidebar),
    path('blogrightsidebar/',views.blogrightsidebar),
    path('blogsingle/',views.blogsingle),
    path('buttons/',views.buttons),
    

    path('cart/',views.cart),
    path('addingproducttocart/',views.addingproducttocart),
    path('cartupdate/',views.cartupdate),
    path('cartremove/',views.cart_remove),
    # path('cart_remove/',views.cart_remove),


    path('checkout/',views.checkout),
    path('comingsoon/',views.comingsoon),
    path('confirmation/',views.confirmation),
    path('contact/',views.contact),
    path('dashboard/',views.dashboard),
    path('emptycart/',views.emptycart),
    path('faq/',views.faq),
    path('forgetpassword/',views.forgetpassword),
    path('jwellery/',views.jwellery),
    path('order/',views.order),
    path('pricing/',views.pricing),
    path('productsingle/',views.productsingle),
    path('profiledetails/',views.profiledetails),
    path('purchaseconfirmation/',views.purchaseconfirmation),
    path('shop/',views.shop),
    path('shopsidebar/',views.shopsidebar),
    path('signin/',views.signin),
    path('typography/',views.typography),

    #model functions
    path('logout/',views.logout),



    #_____________________________________________________
    #admin side
    path('adminloginpage/',views.adminloginpage),
    path('adminregisterpage/',views.adminregisterpage),
    path('adminindex/',views.adminindex),
    path('adminlogout/',views.adminlogout),
    path('adminbase/',views.adminbase),


    #productadding and deleting
    path('adminproduct/',views.adminproduct),
    path('productupdateordelete/',views.productupdateordelete),
    path('productupdating/',views.productupdate),
    path('productdelete/',views.productdelete),


    


    
    
    





   
]
