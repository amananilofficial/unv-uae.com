# from django import forms
# from .models import Product, Category


# class ContactFormModel(forms.ModelForm):
#     class Meta:
#         model = ContactForm
#         fields = ['category', 'product', 'name', 'email', 'phone', 'message']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Add placeholders and custom attributes to the form fields
#         self.fields['message'].widget.attrs.update(
#             {'rows': 4, 'placeholder': 'Enter your message'})

#         # Adding placeholders for other fields
#         self.fields['name'].widget.attrs.update(
#             {'placeholder': 'Enter your full name'})
#         self.fields['email'].widget.attrs.update(
#             {'placeholder': 'Enter your email address'})
#         self.fields['phone'].widget.attrs.update(
#             {'placeholder': 'Enter your phone number'})

#         # Optionally, you can add custom styling to form fields
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})

#         # Optional: Making 'category' and 'product' required fields
#         self.fields['category'].queryset = Category.objects.all()
#         self.fields['product'].queryset = Product.objects.all()

#         # Dynamically filter the product field based on the selected category.
#         # This can be handled in the view or with JavaScript to update the product options.
#         if 'category' in self.data:
#             try:
#                 category_id = int(self.data.get('category'))
#                 self.fields['product'].queryset = Product.objects.filter(
#                     category_id=category_id)
#             except (ValueError, TypeError):
#                 pass  # If the category is invalid, we do not filter products.

#         # Optionally, add any extra validations for form fields if needed
#         self.fields['name'].required = True
#         self.fields['email'].required = True
#         # You can adjust this depending on whether phone is mandatory
#         self.fields['phone'].required = False
#         self.fields['message'].required = True

#     # Additional custom methods can be added if needed
