from django.shortcuts import render,redirect
from ecommerceapp.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from ecommerceapp import keys
from django.conf import settings
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
from PayTm import Checksum


from math import ceil

# Create your views here.
def index(request):

    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides= n // 4 + ceil((n/4) - (n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    
    params={'allProds':allProds}

    return render(request,"index.html",params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        # pnumber = request.POST.get("pnumber")  # Corrected field nam
        print('hello error1')
        myquery = Contact(name=name, email=email, desc=desc)  # Corrected field name
        print('hello eroor 2')
        myquery.save()
        messages.info(request, "We will get back to you soon.")
    return render(request, "contact.html")



def about(request):
    return render(request,"about.html")

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        messages.info(request, "YOur order is Placed ")
        # return redirect('orderplaced/')
        # return render(request,'checkout.html')
        # update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        # update.save()
        # thank=True
# # # PAYMENT INTEGRATION

        # id = Order.order_id
        # oid=str(id)+"ShopyCart"
        # param_dict = {

        #     'MID':keys.MID,
        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            rid=a.replace("ShopyCart","")
           
            print(rid)
            filter2= Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            for post1 in filter2:

                post1.oid=a
                post1.amountpaid=b
                post1.paymentstatus="PAID"
                post1.save()
            print("run agede function")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

# from django.contrib import messages
# from django.shortcuts import render, redirect
# from myapp.models import Orders, OrderUpdate

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login and try again.")
        return redirect('/auth/login')
    
    current_user = request.user.username
    
    # Filter orders for the current user
    items = Orders.objects.filter(email=current_user)
    for i in items:
        print(i.name)
    
    # Retrieve order IDs for the user's orders
    order_ids = [order.order_id for order in items]
    for i in order_ids:
        print('the order id is:\t',i)

    
    # Retrieve order updates for the user's orders
    order_updates = OrderUpdate.objects.filter(order_id__in=order_ids)
    # for i in order_updates:
    #     print(i.order_id)
    #     print(i.update_desc)
    #     order=True
    
    my_dict = {"items": items, "order_updates": order_updates}
    
    return render(request, 'profile.html', context=my_dict)


def orderplaced(request):
    return render(request,"orderplaced.html")

