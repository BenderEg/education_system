from uuid import UUID

from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView


class ProductSubscriptionView(APIView):
    #@extend_schema(request=PaymentIn, responses=schemas.PaymentOutputSchema)
    def post(
        self,
        request: Request,
        product_id: UUID,
        user_id: UUID,
    ):
        # add user_id and product_id to UserProducts

        return JsonResponse(
                data={"detail": "subscription created"},
                status=status.HTTP_200_OK,
            )


class ProductsView(APIView):
    #@extend_schema(request=PaymentIn, responses=schemas.PaymentOutputSchema)
    def get(
        self,
        request: Request,
    ):
        # return info about products

        return JsonResponse(
                data={"detail": "hear are products"},
                status=status.HTTP_200_OK,
            )

class UserLessons(APIView):
    #@extend_schema(request=PaymentIn, responses=schemas.PaymentOutputSchema)
    def get(
        self,
        request: Request,
        product_id: UUID,
        user_id: UUID,
    ):
        # return info about user lessons

        return JsonResponse(
                data={"detail": "hear are lessons for this product"},
                status=status.HTTP_200_OK,
            )