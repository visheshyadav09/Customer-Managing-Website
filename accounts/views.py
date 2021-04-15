from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
# Create your views here.
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def loginPage(request):
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password Incorrect!')

    context={}
    return render(request,'accounts/login.html',context)
    

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        # this gives us an already made up form by django
        form=CreateUserForm()
        # this helps us create an user in the admin panel
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                # this line is used to fetch the username from the form
                username=form.cleaned_data.get('username')

                #these two lines create a new group of customer and add a new user to it
                group=Group.objects.get(name='customer')
                user.groups.add(group)
                # this creates a customer on registratin
                Customer.objects.create(
                    user=user,
                )

                #this line helps in sending a flash message or a one time message to the template so that it can be  displayed over login page
                messages.success(request,"Account was created for "+username)
                return redirect('login')
            
        context={'form':form}

        return render(request,'accounts/register.html',context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/users.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    #this line gets us the logged in user at any point of time
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        #the request.POST gets the post data
        form =CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()
    context={'form':form}
    return render(request,'accounts/accounts_settings.html' , context)

# the login_url="login" is the url to which we want to redirect if we are not logged in ,
# We can also built these login_required fields manually 
@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={'orders':orders,'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    orders_count=orders.count()
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs

    context={'customer':customer,'orders':orders,'orders_count':orders_count,'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    customer=Customer.objects.get(id=pk)
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)#the extra fileld lets us set the number extra input fields to be displayed
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)#the queryset=Order.objects.none() line helps django to not display the already made orders
    #form=OrderForm(initial={'customer':customer})
    if request.method=="POST":
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'formset':formset}
    return render(request,'accounts/order_form.html' ,context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form =OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('/') 
    context={'item':order}
    return render(request,'accounts/delete.html',context)
