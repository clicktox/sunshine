from django import forms
from models import *
from cissonius.utils import fetch_product_image

class ProductFromUrlForm(forms.Form):
    url = forms.URLField(required=True)
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('image',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('image',)
        
class ProductImageFromUrlForm(forms.Form):
    url = forms.URLField(required=True)
    
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

class ProductLinkForm(forms.ModelForm):
    class Meta:
        model = ProductLink
        exclude=('product',)  
class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        exclude = ('image',)

class ProductReviewForm(forms.ModelForm):
    add_to_musthaves = forms.BooleanField(required=False)
    class Meta:
        model = ProductReview
        exclude= ('product','user','reviewed_on','public')

    