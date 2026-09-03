from django.shortcuts import render,redirect,get_object_or_404
from .models import * 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def minis(request):
    mini_list={
        'mini':Product.objects.filter(categories__name="mini")[:4],
        'newarrivals':Product.objects.filter(categories__name="newarrivals")[:4],
        'best':Product.objects.filter(categories__name="best")[5:9],
        'videos':Product.objects.filter(categories__name="video")[:4]
    }
    return render(request,'home.html',mini_list)


def minipage(request):
    minipages={
        'miniature':Product.objects.filter(categories__name="mini")
    }
    return render(request,'mini.html',minipages)

def newarrivals(request):
    newpage={
        'newarrival':Product.objects.filter(categories__name="newarrivals")
    }
    return render(request,'new.html',newpage)

def bestselling(request):
    bestsell={
        'bestselle':Product.objects.filter(categories__name="best")
    }
    return render(request,'best.html',bestsell)

def sweet(request):
    sweets={
        'sweet':Product.objects.filter(categories__name='sweet')
    }
    return render(request,'sweet.html',sweets)

def woody(request):
    woodys={
        'woody':Product.objects.filter(categories__name='woody')
    }
    return render(request,'woody.html',woodys)

def floral(request):
    florals={
        'floral':Product.objects.filter(categories__name='floral')
    }
    return render(request,'floral.html',florals)

def citric(request):
    citrics={
        'citric':Product.objects.filter(categories__name='citric')
    }
    return render(request,'citric.html',citrics)

def fruity(request):
    fruitys={
        'fruity':Product.objects.filter(categories__name='fruity')
    }
    return render(request,'fruity.html',fruitys)
def musk(request):
    musks={
        'musk':Product.objects.filter(categories__name='musk')
    }
    return render(request,'musk.html',musks)
def anymini(request):
    anyminis={
        'anymini':Product.objects.filter(categories__name='pic any mini')
    }
    return render(request,'picanymini.html',anyminis)
def shopall(request):
    shopal={
        'shopall':Product.objects.all()
    }
    return render(request,'shopall.html',shopal)

from .forms import CreateUserForm

def userregister(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            Cart.objects.create(user=user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CreateUserForm()

    return render(request, 'Register.html', {'form': form})

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm           
def user_login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(minis)
    else:        
        form=AuthenticationForm()
    return render(request,'Login.html',{'form':form})
product_id=None

def user_logout(request):
    logout(request)
    return redirect('login')

def product_detail(request, id):
    product_id = get_object_or_404(Product, pk=id)
    product=product_id
    if request.user.is_authenticated:
        return render(request, 'product_detail.html', {'product': product})
    else:
        return redirect('login')

def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    Cartitem.objects.filter(cart=cart, product=product).delete()

    return redirect('cart_page')
    

def increase_quantity(request, product_id):
    cart = request.user.cart

    cart_item =Cartitem.objects.filter(
        cart=cart,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')

def decrease_quantity(request, product_id):
    cart = request.user.cart

    cart_item =Cartitem.objects.filter(
        cart=cart,
        product_id=product_id
    ).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart_page')

def cart(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=id)

    action = request.POST.get('action')
                 
    if action == "buy_now":
        return redirect(f'/checkout/?mode=buy_now&product_id={product.id}')

    cart, created = Cart.objects.get_or_create(user=request.user)

    cartitem, created = Cartitem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        cartitem.quantity += 1
        cartitem.save()

    return redirect('cart_page')

def addtocart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart,created=Cart.objects.get_or_create(user=request.user)
    items =Cartitem.objects.filter(cart=cart).order_by('-id')
    
    mrp = 0
    total_discount = 0
    fees = 10
    
    for item in items:
        mrp+=item.product.price*item.quantity
        
        discount_per_unit=item.product.price-item.product.dprice
        total_discount+=discount_per_unit*item.quantity

    total_amount=mrp-total_discount+fees
    
    save=total_discount

    full={
        'items':items,
        'mrp':mrp,
        'dis':total_discount,
        'fee':fees,
        'total':total_amount,
        'save':save
    }
    
    return render(request, 'cart.html', full)

@login_required
def profile(request):
    if request.user.is_authenticated:
        profile,created=UserProfile.objects.get_or_create(user=request.user)
        print(request.user)
        return render(request,'profile.html',{'profile':profile})
    else:
        return redirect('login')

def profile_form(request):
    ob=None
    if request.user.is_authenticated:
        ob,created=UserProfile.objects.get_or_create(user=request.user)
        if request.method=='POST':
            profile=request.FILES.get('profile')
            from django.contrib.auth.models import User

            new_username = request.POST.get('username')

            if new_username:
                if not User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                    request.user.username = new_username
                    request.user.save()
                    
            location=request.POST.get('location')
            phone=request.POST.get('phone')
            pincode=request.POST.get('pincode')
            email=request.POST.get('email')
            state=request.POST.get('state')
            district=request.POST.get('country')

            if profile:
                ob.profile_picture = profile
            ob.Email=email
            ob.state=state
            ob.country=district
            ob.user=request.user
            ob.pincode=pincode
            ob.location=location
            if len(phone)==10:
                ob.phone_number=phone
            ob.save()
            return redirect('profile')
        else:
            ob= UserProfile.objects.get(user=request.user)
    return render(request,'profiles.html',{'ob':ob})

def search(request):
    query = request.GET.get('q')
    product = Product.objects.none()

    if query:
        results = (
            Product.objects.filter(name__icontains=query) |
            Product.objects.filter(categories__name__icontains=query) |
            Product.objects.filter(genter__icontains=query) |
            Product.objects.filter(ML__icontains=query) |
            Product.objects.filter(notes__icontains=query) |
            Product.objects.filter(season__icontains=query) |
            Product.objects.filter(occasion__icontains=query)
        )

        if query.isdigit():
            results = results | Product.objects.filter(dprice=query)

        product = results.distinct()

    return render(request, 'search.html', {
        'product': product,
        'query': query
    })
from datetime import date, timedelta

def thankyou(request):
    return render(request,'thankyou.html')

APPLICATION_FEE = 10

from datetime import date, timedelta

APPLICATION_FEE = 10

@login_required
def checkout(request):

    ob, created = UserProfile.objects.get_or_create(user=request.user)

    mode = request.POST.get('mode') or request.GET.get('mode')
    product_id = request.POST.get('product_id') or request.GET.get('product_id')

    is_buy_now = (mode == "buy_now")

    product = None
    cart_items = []

    if is_buy_now and product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        cart_items = Cartitem.objects.filter(cart__user=request.user)

    total = 0

    if is_buy_now and product:
        total = product.dprice
    else:
        for item in cart_items:
            total += item.get_total()

    fee = APPLICATION_FEE
    grand_total = total + fee

    print("----- CHECKOUT DEBUG -----")
    print("METHOD:", request.method)
    print("GET:", request.GET)
    print("MODE:", mode)
    print("PRODUCT_ID:", product_id)
    print("IS BUY NOW:", is_buy_now)
    print("PRODUCT:", product)
    print("CART ITEMS COUNT:", len(cart_items))

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_amount=grand_total,
            delivery_date=date.today() + timedelta(days=5)
        )

        if is_buy_now and product:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.dprice
            )
            Cartitem.objects.filter(
            product_id=product_id,
            cart=request.user.cart
            ).delete()

        else:
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.dprice
                )

            cart_items.delete()

        return redirect('thankyou')

    return render(request, 'checkout.html', {
    'cart_items': cart_items,
    'product': product,
    'total': total,
    'fee': fee,
    'grand_total': grand_total,
    'ob': ob,
    'is_buy_now': is_buy_now,
    'mode': mode,             
    'product_id': product_id 
})
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)\
        .prefetch_related('orderitem_set__product')\
        .order_by('-created_at')

    return render(request, "order.html", {
        "orders": orders
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

@login_required
def wish_add(request,id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    return redirect('product_detail', id=product.id)


@login_required
def wish_list(request):
    items = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request,'wishlist.html',{'items':items})


@login_required
def delete_wish(request,id):
    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )
    item.delete()
    return redirect('wishlist_page')


def privacy(request):
    return render(request,'privacy.html')

def about(request):
    return render(request,'about.html')