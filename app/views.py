from django.shortcuts import render,redirect
from.import views
from django.http import HttpResponseRedirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import os
import razorpay
from django.views.decorators.cache import never_cache

from django.http import JsonResponse
import json
import requests






# Create your views here.
def index(request):
    return render(request,'index.html')


#login and logout-------------------------------------------------------------------

def login(request):
    if request.method == 'POST':
        login_email = request.POST['email']
        login_password = request.POST['password']


        # subject = 'Logged one person'
        # message = f'email:{login_email},'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [settings.EMAIL_HOST_USER, ]
        # send_mail(subject, message,email_from, recipient_list)
        # ####
        # subject = 'WELCOME TO AVITO'
        # message = f'hello -{login_email}, Thanks for choosing us, lets shop'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [login_email, ]
        # send_mail(subject,message,email_from,recipient_list)



        check = signintable.objects.filter(email=login_email,password=login_password)
        if check:
            for i in check:
                request.session['id']=i.id
                request.session['fname']=i.fname
            return render(request,'index.html')    
        else:
            return render(request,'login.html')
    else:

        return render(request,'login.html')
    

@never_cache    
def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        del request.session['fname']
    return HttpResponseRedirect('/')
# -----------------------------------------------------------------------------------
    



def noload(request):
    return render(request,'404.html')

def about(request):
    return render(request,'about.html')

def address(request):
    return render(request,'address.html')

def alerts(request):
    return render(request,'alerts.html')

def base(request):
    return render(request,'base.html')

def blogfullwidth(request):
    return render(request,'blogfullwidth.html')

def bloggrid(request):
    return render(request,'bloggrid.html')

def blogleftsidebar(request):
    return render(request,'blogleftsidebar.html')

def blogrightsidebar(request):
    return render(request,'blogrightsidebar.html')

def blogsingle(request):
    return render(request,'base.html')

def buttons(request):
    return render(request,'buttons.html')


#_________________________________________________________________________
def buyall(request):
    if request.session.has_key('id'):
        user = request.session['id']
        dataall = carttable.objects.filter(user_id=user)
        total = 0
        for i in dataall:
            total += float(i.total)

        client = razorpay.Client(auth=("rzp_test_QtSg1knCBDQ1Yv", "v2rrB9McFhnb0Wqdho7Wl8yj"))
        # Create an order
        order_amount = 10000 # Amount in paise (e.g., 1000 paise = ₹10)
        order_currency = "INR"
        order_receipt = "order_receipt_12345" # Generate a unique receipt ID for each order
        
        payment_order = client.order.create({
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': 1 # Auto capture payments
        })
        payment_order_id = payment_order['id']
        context = {
            'amount':500,
            'api_key': 'rzp_test_7hCWqiwACtPv',
            'order_id':payment_order_id
        }


        return render(request,'buyall.html',{'buydata':dataall,'total':total,"context":context})
    else:
        return render(request,'buyall.html')
      
    


#__________________________________________________________________________

def cart(request):
    if request.session.has_key('id'):
        user = request.session['id']
        data = carttable.objects.filter(user_id=user)
        total = 0
        for x in data:
            # qty = x.quantity
            # price = x.items_id.productprice

            total += float(x.total)
        cartstore = carttable.objects.filter(user_id =user)
        return render(request,'cart.html',{'cartdata':cartstore,'total':total})
    else:
        return render(request,'shop.html')
#___________________________________________________________________________
 #cart remove
# def cart_remove(request):
    
#     return render(request,'shop.html')




#___________________________________________________________________________
#addin product to cart
def addingproducttocart(request):
    if request.session.has_key('id'):
        if request.method == 'POST':
            product_itemid = request.GET['prdid'] 
            prodct = addingproducttable.objects.get(id=product_itemid)
            user_id = request.session['id']
            user = signintable.objects.get(id=user_id)

            product = addingproducttable.objects.filter(id=product_itemid)
            for x in product:
                price = x.productprice
            total = 0
            total = int(price)

            check = carttable.objects.filter(items_id=product_itemid,user_id=user_id)
            if check:
                for i in check:
                    qty = i.quantity
                    tot = i.total
                    prz = i.items_id.productprice
                qty+=1
                tot+=int(prz)
                add = carttable.objects.filter(items_id=product_itemid,user_id=user_id).update(quantity=qty,total=tot)
                
                cartstore = carttable.objects.filter(user_id = user)
                # totaldata = carttable.objects.filter(user_id=user)
                total3 = 0
                for x in cartstore:
                    total3 += float(x.total)
                return render (request,'cart.html',{'cartdata':cartstore,'total':total3})

            

            else:
                add = carttable(items_id=prodct, user_id=user,total = total)
                add.save()

                data = signintable.objects.filter(id=user_id)
                for x in data:
                    uid=x.id
                cartstore = carttable.objects.filter(user_id = uid)
                totaldata = carttable.objects.filter(user_id=user)
                total3 = 0
                for x in totaldata:
                    total3 += float(x.total)
                return render (request,'cart.html',{'cartdata':cartstore,'total':total3})
        else:
            return HttpResponseRedirect('shop.html')
    else:

        return HttpResponseRedirect('shop.html')        

#_____________________________________________________________________________________
#cart update

def cartupdate(request):
    if request.method == 'POST':
        cart_id = request.GET['prdid'] 
        quantity = request.POST['size']
        cart = carttable.objects.filter(id=cart_id)
        newprice=0
        for i in cart:
            price=i.items_id.productprice
            
            print("ppppppppp",price)
        newprice = float(price)*int(quantity)
        carttable.objects.filter(id=cart_id).update(quantity=quantity,total=newprice)
    
        return redirect('/cart/')


    else:
        return render(request,'shop.html')
# _____________________________________________________________________________________
#cart remove
def cart_remove(request):
    cart_id = request.GET['prdid']
    carttable.objects.filter(id=cart_id).delete()
    return HttpResponseRedirect('/cart/')

# _____________________________________________________________________________________

def checkout(request):
    check_id = request.GET['checkid']
    add=carttable.objects.filter(id=check_id)
    return render(request,'checkout.html',{'cartdata':add})
#______________________________________________________________________________________

def comingsoon(request):
    return render(request,'comingsoon.html')

def confirmation(request):
    return render(request,'confirmation.html')

def contact(request):
    return render(request,'contact.html')

def dashboard(request):
    return render(request,'dashboard.html')

def emptycart(request):
    return render(request,'emptycart.html')

def faq(request):
    return render(request,'faq.html')

def forgetpassword(request):
    return render(request,'forgetpassword.html')

def jwellery(request):
    return render(request,'jwellery.html')

def order(request):
    return render(request,'order.html')

def pricing(request):
    return render(request,'pricing.html')

def productsingle(request):
    return render(request,'productsingle.html')

def profiledetails(request):
    return render(request,'profiledetails.html')

def purchaseconfirmation(request):
    return render(request,'purchaseconfirmation.html')


#__________________________________________________________________________
#shoping gallery

def shop(request):
    shopdisplay = addingproducttable.objects.all()
    return render(request,'shop.html',{'data':shopdisplay})


#__________________________________________________________________________

def shopsidebar(request):
    return render(request,'shopsidebar.html')

# -------------------------------------------------------------------------
#registration

def signin(request):
    if request.method == 'POST':
        signin_fname = request.POST['fname']
        signin_lname = request.POST['lname']
        signin_uname = request.POST['uname']
        signin_email = request.POST['email']
        signin_password = request.POST['password']     
        add = signintable(fname=signin_fname,Lname=signin_lname,Uname=signin_uname,email=signin_email,password=signin_password)
        add.save()
        
        return render(request,'index.html')
    else:

        return render(request,'signin.html')
    

# ---------------------------------------------------------------------------------

def typography(request):
    return render(request,'typography.html')










#-------------------------------------------------------------------------------
#_______________________________________________________________________________
#-------------------------------------------------------------------------------
#admin login and admin logout

def adminloginpage(request):
    if request.method == 'POST':
        admin_email = request.POST['email']
        admin_password = request.POST['password']
        
        check = adminregistertable.objects.filter(email=admin_email,password=admin_password)
        if check:
            for i in check:
                request.session['aid']=i.id
                request.session['name']=i.name
            return render(request,'admin/index.html')    
        else:
            return render(request,'admin/adminloginpage.html')
    else:
        return render(request,'admin/adminloginpage.html')

#logout

def adminlogout(request):
    if request.session.has_key('aid'):
        del request.session['aid']
        del request.session['name']
    return redirect('/adminloginpage/')

# ___________________________________________________________________________


#adminregister
def adminregisterpage(request):
    if request.method == 'POST':
        admin_name = request.POST['name']
        admin_email = request.POST['email']
        admin_password = request.POST['password']     
        add = adminregistertable(name=admin_name,email=admin_email,password=admin_password)
        add.save()
        
        return render(request,'admin/adminloginpage.html')
    else:
        return render(request,'admin/adminregisterpage.html')
    

#_________________________________________________________________________________
#admin dashboard page
def adminindex(request):
    return render(request,'admin/index.html')

#_________________________________________________________________________________

def adminproduct(request):
    if request.method == 'POST':
        product_name = request.POST['p_name']
        product_price = request.POST['p_price']
        product_category = request.POST['p_category']
        product_description = request.POST['p_description']
        product_image = request.FILES['p_image']
        product_size = request.POST['p_size']
        add = addingproducttable(productname=product_name,productprice=product_price,productcatagory=product_category,productdescription=product_description,productimage=product_image,productsize=product_size) 
        add.save()
        return render(request,'admin/index.html')
    else:
        return render(request,'admin/productamange.html')
    

#______________________________________________________________________________________ 
def adminbase(request):
    return render(request,'admin/adminbase.html')

#______________________________________________________________________________________






#______________________________________________________________________________________
#product updating or deleting page section
def productupdateordelete(request):
    Updateordelete=addingproducttable.objects.all()
    return render(request,'admin/productupdateordelete.html',{'Upordel':Updateordelete})



#_______________________________________________________________________________________
#product updating and delete function


def productupdate(request):
    if request.method == 'POST':
        updating_product_name = request.POST['name']
        updating_product_price = request.POST['price']
        updating_product_category = request.POST['category']
        updating_product_description = request.POST['description']
        updating_product_size = request.POST['size']
        product_id = request.GET['upid']
        checkbox = request.POST['updateimage']
        if checkbox == 'yes':
            updating_product_image = request.FILES['image']
            old_product_data = addingproducttable.objects.filter(id=product_id)
            update_product_data = addingproducttable.objects.get(id=product_id)
            for x in old_product_data:
                imageurl = x.productimage.url
                imagepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imageurl
                if os.path.exists(imagepath):
                    os.remove(imagepath)
                    print('image removed')
            update_product_data.productimage = updating_product_image
            update_product_data.save()              
        product_data = addingproducttable.objects.filter(id=product_id).update(productname=updating_product_name,productcatagory=updating_product_category,productdescription=updating_product_description,productsize=updating_product_size)
        return HttpResponseRedirect('/productupdateordelete/')
    else:
        product_id = request.GET['upid']
        product_data = addingproducttable.objects.filter(id=product_id)
        return render(request,'admin/productupdate.html',{'Upordel':product_data})
    

def productdelete(request):
    if request.session.has_key('aid'):
        product_id = request.GET['upid']
        old_product_data = addingproducttable.objects.filter(id=product_id)
        for x in old_product_data:
            imageurl = x.productimage.url
            imagepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imageurl
            if os.path.exists(imagepath):
                os.remove(imagepath)
                print('image deleted')

        product_data = addingproducttable.objects.filter(id=product_id).delete()
        return redirect('/productupdateordelete/')
    else:
        return redirect('/adminindex/')

#_________________________________________________________________________________________
#PAYMENTS

client = razorpay.Client(auth=("rzp_test_7hCWqiwACtPv", "A34QNrCreBhMLXrKhXl1lXut"))
def payment(request):


# Initialize Razorpay client
    
    
    # Create an order
    order_amount = 10000 # Amount in paise (e.g., 1000 paise = ₹10)
    order_currency = "INR"
    order_receipt = "order_receipt_12345" # Generate a unique receipt ID for each order
    
    payment_order = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': 1 # Auto capture payments
    })
    payment_order_id = payment_order['id']
    context = {
        'amount':500,
        'api_key': 'rzp_test_7hCWqiwACtPv',
        'order_id':payment_order_id
    }
    
    return render(request,'buyall.html',context)
   

   









