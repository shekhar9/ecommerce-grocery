from django import forms
from django.contrib.auth.models import User
from .models import Product, Order,Category,Brand,Banners

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    is_admin = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already in use')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already in use')
        return email
    
    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        user.is_staff = data['is_staff']
        user.is_admin = data['is_admin']
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'sku', 'ean_number',
            'main_image', 'price', 'mrp', 'charge_tax', 'stock',
            'weight', 'weight_unit', 'size_in', 'length', 'width', 'height',
             'brand', 'tags', 'status', 'meta_title',
            'meta_description', 'url_handle'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_head','title', 'seller_percentage', 'media']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name','logo']
    

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'status']


class BnnersForm(forms.ModelForm):
    class Meta:
        model=Banners
        fields=['title','banner_type','image']