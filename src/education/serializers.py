from rest_framework import serializers

from .models import UserProduct, Lesson


class UserProductSerializer(serializers.ModelSerializer):

    product_id = serializers.UUIDField()

    class Meta:
        model = UserProduct
        fields = [
            "user_id",
            "product_id",
            "id"
        ]


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"