import os
import django
from django.core.files import File

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_website.settings')
django.setup()

from App.models import Product  # Предполагается, что модель называется Product

def create_products():
    products_data = [
        {'name': 'Сумка SStyle стандарт', 'price': 10100, 'image': 'photo1_1.jpg'},
        {'name': 'Сумка SStyle мини', 'price': 9100, 'image': 'photo2_2.jpg'},
        {'name': 'Сумка Hobo Bag', 'price': 7900, 'image': 'photo6_6.jpg'},
        {'name': 'Сумка Vogue Bag размер S', 'price': 8900, 'image': 'photo3.png'},
        {'name': 'Сумка Vogue Bag размер M', 'price': 9400, 'image': 'photo4_4.jpg'},
        {'name': 'Сумка Vogue Bag размер L', 'price': 10200, 'image': 'photo5.png'},
        {'name': 'Косметичка Big Beauty Bag', 'price': 3900, 'image': 'photo7.png'},
        {'name': 'Косметичка Домик', 'price': 3900, 'image': 'photo8.png'},
        {'name': 'Косметичка Ракушка', 'price': 3400, 'image': 'photo9.png'},
        {'name': 'Косметичка For Dyson', 'price': 4300, 'image': 'photo10.png'},
        {'name': 'Косметичка For Bork', 'price': 4300, 'image': 'photo11.png'},
        {'name': 'Косметичка Beauty case из эко-кожи', 'price': 3900, 'image': 'photo13.png'},
        {'name': 'Рюкзак Around the world', 'price': 10600, 'image': 'photo12_12.jpg'},
        {'name': 'Чехол под телефон', 'price': 3500, 'image': 'photo14.jpg'},
        {'name': 'Чехол на ноутбук', 'price': 5200, 'image': 'photo15.jpg'},
    ]

    # Путь к папке со статическими файлами (измените на ваш реальный путь)
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'my_website', 'App', 'static')

    for data in products_data:
        try:
            product = Product(
                name=data['name'],
                price=data['price']
            )

            image_path = os.path.join(static_dir, data['image'])

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    product.image.save(data['image'], File(f))
                product.save()
                print(f"Успешно создан товар: {product.name}")
            else:
                print(f"Ошибка: файл {data['image']} не найден в {image_path}")
        except Exception as e:
            print(f"Ошибка при создании товара {data['name']}: {str(e)}")

if __name__ == '__main__':
    print("Начало заполнения базы данных...")
    create_products()
    print("Заполнение завершено!")