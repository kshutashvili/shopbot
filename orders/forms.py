# -*- coding: utf-8 -*-
import re

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    error_css_class = 'error'
    class Meta:
        model = Order
        fields = ['product', 'customer_name', 'customer_phone',]
        widgets = {'product': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs = {'class': 'form-input', 'placeholder': u'Ваше имя'}
        self.fields['customer_phone'].widget.attrs = {'class': 'form-input', 'placeholder': u'Ваш номер мобильного телефона'}

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone', None)
        pattern = re.compile(r'^(\+\d{1,2})?[\s.-]?(\d{3})[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}$')
        matched = pattern.search(phone)
        if matched:
            return phone
        else:
            raise forms.ValidationError("Номер телефона должен быть в формате: "\
                                        "+7 495 222 33 44")
