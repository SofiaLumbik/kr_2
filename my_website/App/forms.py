from django import forms
from .models import Order, Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'product']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

        # Добавляем классы и placeholder'ы
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Проверка базового формата email
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Пожалуйста, введите корректный email-адрес")

        # Дополнительная проверка на минимальную длину
        if len(email) < 6:  # a@b.ru - минимально возможный email
            raise forms.ValidationError("Email слишком короткий")

        return email


class OrderFilterForm(forms.Form):
    SORT_CHOICES = [
        ('-created_at', 'Новые сначала'),
        ('-created_at', 'Старые сначала'),
        ('last_name', 'Фамилия (А-Я)'),
        ('-last_name', 'Фамилия (Я-А)'),
        ('total_price', 'Сумма (дешевые)'),
        ('-total_price', 'Сумма (дорогие)'),
    ]

    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='-created_at')
    customer = forms.CharField(required=False, label="Фамилия клиента")
    date = forms.DateField(required=False, label="Дата заказа", widget=forms.DateInput(attrs={'type': 'date'}))


class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100, required=False)