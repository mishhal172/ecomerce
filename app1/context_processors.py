from .models import Product

def minicombo(request):
    return {
        'minicombo': Product.objects.only('image', 'genter')[:5]
    }