from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Count, Sum
from .models import HomePage, ContactPage, Product, Order, Classmate, EducationProgram
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .forms import SearchForm



def base(request):
    return render(request, 'base.html')


def main(request):
    home_content = HomePage.objects.first()
    if not home_content:
        home_content = HomePage.objects.create(
            banner_title="Around the World",
            banner_subtitle="идеальный аксессуар, чтобы подчеркнуть вашу индивидуальность",
            about_title="О бренде",
            about_content="""<p>Наши аксессуары разработаны с учётом всех современных требований...</p>""",
            order_title="Как сделать заказ?",
            gift_title="Подарочный сертификат",
            gift_content="""<p>Не упустите возможность удивить своих близких...</p>"""
        )
    return render(request, 'main.html', {'home': home_content})


def catalog(request):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '')
    category = request.GET.get('category', '')

    products = Product.objects.all()

    if query:
        search_terms = query.split()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(name__icontains=term)
        products = products.filter(q_objects)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    if category:
        if category == 'sumki':
            products = products.filter(Q(name__icontains='сумка') | Q(name__icontains='Сумка'))
        elif category == 'cosmetic':
            products = products.filter(Q(name__icontains='косметичка') | Q(name__icontains='Косметичка'))
        elif category == 'rykzaki':
            products = products.filter(Q(name__icontains='рюкзак') | Q(name__icontains='Рюкзак'))
        elif category == 'chehly':
            products = products.filter(Q(name__icontains='чехол') | Q(name__icontains='Чехол'))

    return render(request, 'catalog.html', {
        'products': products,
        'query': query
    })


from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum, Count, Max, Min
from django.contrib import messages
from datetime import timedelta

def contacts(request):
    contact_data = ContactPage.objects.first()
    products = Product.objects.all()
    orders = Order.objects.all()

    # Обработка POST-запроса — создание нового заказа
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        product_id = request.POST.get('product')

        try:
            product = Product.objects.get(id=product_id)
            Order.objects.create(
                last_name=last_name,
                first_name=first_name,
                email=email,
                product=product
            )
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect(reverse('App:contacts') + '#order-section')
        except Product.DoesNotExist:
            messages.error(request, 'Выбранный товар не найден.')
        except Exception as e:
            messages.error(request, f'Ошибка при оформлении заказа: {e}')

    # Фильтрация заказов
    last_name_filter = request.GET.get('last_name_filter', '').strip()
    if last_name_filter:
        orders = orders.filter(last_name__icontains=last_name_filter)

    date_filter = request.GET.get('date_filter', '')
    now = timezone.now()
    if date_filter == 'today':
        orders = orders.filter(created_at__date=now.date())
    elif date_filter == 'week':
        week_ago = now - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = now - timedelta(days=30)
        orders = orders.filter(created_at__gte=month_ago)

    # Сортировка заказов
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['created_at', '-created_at', 'last_name', '-last_name']
    if sort not in allowed_sorts:
        sort = '-created_at'
    orders = orders.order_by(sort)

    # Фильтр по цене заказа
    price_filter = request.GET.get('price_filter', '')  # 'most_expensive' или 'cheapest'
    if price_filter == 'most_expensive':
        max_price = orders.aggregate(max_price=Max('product__price'))['max_price']
        if max_price is not None:
            orders = orders.filter(product__price=max_price)
    elif price_filter == 'cheapest':
        min_price = orders.aggregate(min_price=Min('product__price'))['min_price']
        if min_price is not None:
            orders = orders.filter(product__price=min_price)

    # Статистика
    total_orders = orders.count()
    total_revenue = orders.aggregate(total=Sum('product__price'))['total'] or 0

    # Популярные продукты считаем исходя из уже отфильтрованных заказов
    # Группируем заказы по продуктам и считаем количество заказов на каждый продукт
    popular_products_qs = (
        orders.values('product')
        .annotate(order_count=Count('id'))
        .order_by('-order_count')
    )

    popular_products = []
    if popular_products_qs.exists():
        max_order_count = popular_products_qs.first()['order_count']  # максимальное количество заказов у товара
        if max_order_count > 1:
            # Есть товары с количеством заказов > 1 — показываем топ-3 популярных
            product_ids = [item['product'] for item in popular_products_qs[:3]]
        else:
            # Нет повторяющихся товаров — показываем все уникальные заказанные товары
            product_ids = [item['product'] for item in popular_products_qs]

        products_dict = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        for item in popular_products_qs:
            pid = item['product']
            if pid in product_ids:
                product_obj = products_dict.get(pid)
                if product_obj:
                    product_obj.order_count = item['order_count']
                    popular_products.append(product_obj)
    else:
        popular_products = []
    context = {
        'contact': contact_data,
        'products': products,
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'popular_products': popular_products,
        'request': request
    }

    return render(request, 'contacts.html', context)




def program_view(request):
    from django.db.models import Q

    program = EducationProgram.objects.first()
    classmates = Classmate.objects.all()
    form = SearchForm(request.GET or None)
    query = form['query'].value() if form.is_valid() else ''

    has_phone = request.GET.get('has_phone', '')  # 'yes', 'no' или ''

    search_results = None  # По умолчанию — результатов нет

    if query:
        found = False
        q_lower = query.lower()
        search_results = {
            'supervisor': None,
            'manager': None,
            'classmates': [],
            'not_found': False,
        }

        if program and program.supervisor_surname and q_lower in program.supervisor_surname.lower():
            search_results['supervisor'] = program
            found = True

        if program and program.manager_surname and q_lower in program.manager_surname.lower():
            search_results['manager'] = program
            found = True

        classmates_found = classmates.filter(surname__icontains=query)
        if classmates_found.exists():
            search_results['classmates'] = classmates_found
            found = True

        if not found:
            search_results['not_found'] = True

    elif has_phone == 'yes':
        # Показываем только сокурсников с номером
        classmates_filtered = classmates.exclude(Q(phone__isnull=True) | Q(phone=''))
        search_results = {
            'supervisor': None,
            'manager': None,
            'classmates': classmates_filtered,
            'not_found': False,
        }

    elif has_phone == 'no':
        # Показываем руководителя, менеджера и сокурсников без номера
        classmates_filtered = classmates.filter(Q(phone__isnull=True) | Q(phone=''))
        search_results = {
            'supervisor': program,
            'manager': program,
            'classmates': classmates_filtered,
            'not_found': False,
        }

    # Если нет ни запроса, ни фильтра — search_results останется None, и в шаблоне ничего не выведется

    context = {
        'program': program,
        'classmates': classmates,
        'form': form,
        'search_results': search_results,
    }
    return render(request, 'program.html', context)
