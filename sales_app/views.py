from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Product,CartItem,Cart
# Create your views here.
def first(request):
#welcome
    if request.method == 'POST':
        message = request.POST.get('message-input')  
        if message == 'hello':
            response = 'Hello user, welcome ! How can i help You? '  
#TELL ME ABOUT  SPECIFIC PRODUCT DETAILS
        elif message.startswith('tell me about '):
            words = message.split()# tell me about is splitted
            product_name = ' '.join(words[3:])#words after tell me about is taken as product_name
            try:
                product=Product.objects.get(name=product_name)
                response= f"Product Name: {product.name}\nDescription: {product.description}\nPrice: {product.price}\nAvailability: {'Available' if product.availability_status else 'Not Available'}"
            except Product.DoesNotExist:
                response = f"Sorry, I couldn't find a product named {product_name}."
#KNOWING THE DETAILS OF PRODUCTS
        elif message == 'what products do you have?':
            products = Product.objects.values_list('name', flat=True)
            response = ', '.join(products)
#RECOMENDING A PRODUCT 
        elif message == 'Can you recommend a product for me?':
#EXCEPTION HANDLING IS USED TO  HANDLE EXCEPTION
            try:
                product = Product.objects.get(name="Mobile Phone")
                response = f"Product Name: {product.name}, Description: {product.description}, Price: {product.price}, Availability: {'Available' if product.availability_status else 'Not Available'}"
            except Product.DoesNotExist:
                response = "Sorry, I couldn't find a product named Mobile Phone."

#ADDING PRODUCT TO CART
        elif message.startswith('add '):
            product_name = message[4:]# message after add taken as product name
#EXCEPTION HANDLING IS USED TO  HANDLE EXCEPTION
            try:
                product = Product.objects.get(name=product_name)
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cart_item.quantity += 1
                cart_item.save()
                response = f"{product.name} has been added to your cart."
            except Product.DoesNotExist:
                response = f"Sorry, I couldn't find a product named {product_name}."
#VIEWING THE CART
        elif message == 'show me my cart':
#EXCEPTION HANDLING IS USED TO  HANDLE EXCEPTION
            try:
               cart = Cart.objects.get(user=request.user)
               cart_items = CartItem.objects.filter(cart=cart)
               response = '\n'.join([f"{item.product.name}: {item.quantity}" for item in cart_items])
            except Cart.DoesNotExist:
                response="Sorry no items is added in cart"
#PURCHASING THE PRODUCT
        elif message == 'buy':
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            response = "Your purchase has been completed successfully."
        else:
            response = 'Sorry, I did not understand your question.' 
        return JsonResponse({'response': response})
    return render(request,'chatbot.html')
