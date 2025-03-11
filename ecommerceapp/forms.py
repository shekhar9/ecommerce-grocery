from django import forms
from django.contrib.auth.models import User
from .models import Product, Order, Category, Brand, Banners,Sellers,Discount
import re  # Import regex for password validation

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

        # Password validation
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")

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
    category_head = forms.ModelChoiceField(
        queryset=Category.objects.order_by('category_head').distinct('category_head'),
        required=True,
        label="Category Type"
    )

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'sku', 'ean_number',
            'main_image', 'price', 'mrp', 'charge_tax', 'stock',
            'weight', 'weight_unit', 'size_in', 'length', 'width', 'height',
            'brand', 'tags', 'status', 'meta_title',
            'meta_description', 'category_head', 'rating'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_head'].queryset = Category.objects.all()  
        self.fields['category_head'].label_from_instance = lambda obj: obj.category_head  

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_head', 'title', 'seller_percentage', 'media']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo']

class BannersForm(forms.ModelForm):
    class Meta:
        model = Banners
        fields = ['title', 'banner_type', 'image']


class SellersForms(forms.ModelForm):
    class Meta:
        model = Sellers
        fields = '__all__'


class DiscountForm(forms.ModelForm):
    class Meta:
        model=Discount
        fields='__all__'