from django.db import models
from ckeditor.fields import RichTextField

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название товара")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name


class HomePage(models.Model):
    banner_title = models.CharField(max_length=100, verbose_name="Заголовок баннера")
    banner_subtitle = models.CharField(max_length=200, verbose_name="Подзаголовок баннера")
    about_title = models.CharField(max_length=100, verbose_name="Заголовок 'О бренде'")
    about_content = RichTextField(verbose_name="Текст 'О бренде'")
    order_title = models.CharField(max_length=100, verbose_name="Заголовок 'Как сделать заказ'")
    gift_title = models.CharField(max_length=100, verbose_name="Заголовок 'Подарочный сертификат'")
    gift_content = RichTextField(verbose_name="Текст 'Подарочный сертификат'")

    # Изображения (пути к файлам)
    banner_image = models.ImageField(upload_to='homepage/', verbose_name="Баннер")
    image1 = models.ImageField(upload_to='homepage/', verbose_name="Изображение 1")
    image2 = models.ImageField(upload_to='homepage/', verbose_name="Изображение 2")
    image3 = models.ImageField(upload_to='homepage/', verbose_name="Изображение 3")
    order_image = models.ImageField(upload_to='homepage/', verbose_name="Изображение процесса заказа")
    gift_image = models.ImageField(upload_to='homepage/', verbose_name="Изображение сертификата")

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Контент главной страницы"


class ContactPage(models.Model):
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.TextField(verbose_name="Режим работы")
    payment_info = models.TextField(verbose_name="Информация по оплате")
    contact_image = models.ImageField(upload_to='contacts/', verbose_name="Изображение контактов")
    payment_image = models.ImageField(upload_to='contacts/', verbose_name="Дополнительное изображение оплаты", blank=True, null=True)

    class Meta:
        verbose_name = "Страница контактов"
        verbose_name_plural = "Страница контактов"



class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.last_name}"

    @property
    def total_price(self):
        return self.product.price


class EducationProgram(models.Model):
    # Информация о себе
    my_name = models.CharField(max_length=100)
    my_surname = models.CharField(max_length=100)  # Добавляем поле фамилии
    my_phone = models.CharField(max_length=20)
    my_photo = models.ImageField(upload_to='program/')

    # Руководитель
    supervisor_name = models.CharField(max_length=100)
    supervisor_surname = models.CharField(max_length=100, null=True, blank=True)
    supervisor_email = models.EmailField()
    supervisor_photo = models.ImageField(upload_to='program/')

    # Менеджер
    manager_name = models.CharField(max_length=100)
    manager_surname = models.CharField(max_length=100, null=True, blank=True)
    manager_email = models.EmailField()
    manager_photo = models.ImageField(upload_to='program/')

    # Информация о программе
    program_name = models.CharField(max_length=100)
    program_description = models.TextField()

    def __str__(self):
        return self.program_name


class Classmate(models.Model):
    program = models.ForeignKey(EducationProgram, on_delete=models.CASCADE, related_name='classmates')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='program/')

    def __str__(self):
        return f"{self.surname} {self.name}"
