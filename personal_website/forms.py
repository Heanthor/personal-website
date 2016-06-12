from django import forms

from models import Item


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "quantity"]
        widgets = {
            "name": forms.TextInput(attrs={
                "id": "item_input",
                "maxlength": 200,
                "required": True,
                "placeholder": "Item"
            }),
            "quantity": forms.NumberInput(attrs={
                "id": "quantity_input",
                "min": 1
            })
        }
