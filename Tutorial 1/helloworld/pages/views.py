from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django import forms

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
    
class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": 2000}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 700}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 200}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 80} 
        ] 
    
class ProductIndexView(View): 
    template_name = 'products/index.html' 
    
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] = "List of products" 
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)
        
class ProductShowView(View): 
    template_name = 'products/show.html' 

    def get(self, request, id): 
        try: 
            if int(id) < 1 or int(id) > len(Product.products):
                raise ValueError
            
        except (ValueError, IndexError):  
            return HttpResponseRedirect(reverse('home')) 
        
        viewData = {} 
        product = Product.products[int(id)-1] 
        viewData["title"] = product["name"] + " - Online Store" 
        viewData["subtitle"] = product["name"] + " - Product information" 
        viewData["product"] = product 

        return render(request, self.template_name, viewData)
        
class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True)
    
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise ValidationError("The price must be greater than zero.")
        return price 
    
class ProductCreateView(View): 
    template_name = 'products/create.html' 
    success_template = 'products/success.html'
    
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
    
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]

            new_product = {
                "id": str(len(Product.products)+1),
                "name": name,
                "description": f"Description of {name}",
                "price": price
            }

            Product.products.append(new_product)

            viewData = {
                "title": "Product Created",
                "message": "Product created successfully!"
            }
            
            return render(request, self.success_template, viewData)
        
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 

            return render(request, self.template_name, viewData)   