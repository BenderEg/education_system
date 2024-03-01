from typing import List
from uuid import UUID

from django.db import connection
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from education.models import UserProduct, Product, Lesson
from education.serializers import UserProductSerializer, LessonSerializer
from education.schemas.product import ProductLesson, ListProductLesson

class ProductSubscriptionView(APIView):
    @extend_schema(request=None, responses=UserProductSerializer)
    def post(
        self,
        request: Request,
        product_id: UUID,
        user_id: UUID,
    ):
        serializer = UserProductSerializer(data={
            "user_id": user_id,
            "product_id": product_id
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsView(APIView):
    @extend_schema(request=None, responses=ListProductLesson)
    def get(
        self,
        request: Request,
    ):
        products = Product.objects.raw("SELECT education_product.id, education_product.name, \
                                       education_product.price, education_product.starting_date, \
                                       count(education_lesson.product_id) as lessons_count \
                                       FROM education_lesson RIGHT \
                                       JOIN education_product \
                                       ON education_product.id = education_lesson.product_id \
                                       GROUP BY education_product.id")
        result = [ProductLesson(id=ele.id,
                                name=ele.name,
                                price=ele.price,
                                starting_date=ele.starting_date,
                                lesson_number=ele.lessons_count) for ele in products]
        return Response(
                data=[ele.model_dump() for ele in result],
                status=status.HTTP_200_OK,
            )


class UserLessons(APIView):
    @extend_schema(request=None, responses=LessonSerializer(many=True))
    def get(
        self,
        request: Request,
        product_id: UUID
    ):
        lessons = Lesson.objects.filter(product_id=product_id)
        return Response(
                data=[ele.model_dump() for ele in lessons],
                status=status.HTTP_200_OK,
            )