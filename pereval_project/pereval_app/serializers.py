from rest_framework import serializers
from .models import User, Pereval, Image
import base64
import uuid
import os

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordsSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    height = serializers.IntegerField()

class LevelSerializer(serializers.Serializer):
    winter = serializers.CharField(required=False, allow_blank=True, default="")
    summer = serializers.CharField(required=False, allow_blank=True, default="")
    autumn = serializers.CharField(required=False, allow_blank=True, default="")
    spring = serializers.CharField(required=False, allow_blank=True, default="")

class ImageSerializer(serializers.Serializer):
    data = serializers.CharField()  # base64
    title = serializers.CharField()

class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'user', 'coords', 'level', 'images'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        # Создаём или находим пользователя
        user, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)

        # Создаём перевал
        pereval = Pereval.objects.create(
            user=user,
            status='new',
            latitude=coords_data['latitude'],
            longitude=coords_data['longitude'],
            height=coords_data['height'],
            winter=level_data.get('winter', ''),
            summer=level_data.get('summer', ''),
            autumn=level_data.get('autumn', ''),
            spring=level_data.get('spring', ''),
            **validated_data
        )

        # Сохраняем изображения
        IMAGE_DIR = "uploaded_images"
        os.makedirs(IMAGE_DIR, exist_ok=True)

        for img_data in images_data:
            # Извлекаем base64 строку
            img_base64 = img_data['data']
            img_title = img_data['title']

            # Убираем префикс, если есть (например, "image/jpeg;base64,...")
            if ',' in img_base64:
                header, img_base64 = img_base64.split(',', 1)

            # Декодируем
            img_binary = base64.b64decode(img_base64)

            # Генерируем уникальное имя файла
            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(IMAGE_DIR, filename)

            # Сохраняем файл
            with open(filepath, "wb") as f:
                f.write(img_binary)

            Image.objects.create(
                pereval=pereval,
                title=img_title,
                path=filepath
            )

        return pereval