from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django import forms
from .models import Product

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Simón Botero", 
        }) 

        return context
    
class ContactPageView(TemplateView): 
    template_name = 'pages/contact.html' 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "subtitle": "Contact us", 
            "email": "pepito@gmail.com",
            "phone":  "3108684310",
            "address": "Calle 33",
        }) 

        return context
    
class ProductIndexView(View): 
    template_name = 'products/index.html' 
    
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] = "List of products" 
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)
        
class ProductShowView(View): 
    template_name = 'products/show.html' 

    def get(self, request, id): 
        try: 
            product_id = int(id)
            if product_id < 1 or product_id > len(Product.objects.all()):
                raise ValueError
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):  
            return HttpResponseRedirect(reverse('home')) 
        
        viewData = {} 
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store" 
        viewData["subtitle"] = product.name + " - Product information" 
        viewData["product"] = product 

        return render(request, self.template_name, viewData)
        
class ProductForm(forms.ModelForm): 
    class Meta: 
        model = Product 
        fields = ['name', 'price']
    
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("The price must be greater than zero.")
        
        return price 
    
class ProductCreateView(View): 
    template_name = 'products/create.html' 
    
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form
    
        return render(request, self.template_name, viewData) 
    
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save()

            return redirect('success')
        
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 

            return render(request, self.template_name, viewData)
        
class ProductSuccessView(TemplateView):
    template_name = "products/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Success",
            "message": "Product created successfully"
        })

        return context
        
class ProductListView(ListView): 
    model = Product 
    template_name = 'product_list.html' 
    context_object_name = 'products' # This will allow you to loop through 'products' in your template 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 

        return context