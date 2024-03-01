from django.urls import path

from .views import ProductSubscriptionView, ProductsView, UserLessons

urlpatterns = [
    path("products/",
         ProductsView.as_view()),
    path("products/<uuid:product_id>/subscription/<uuid:user_id>/",
         ProductSubscriptionView.as_view()),
    path("products/<uuid:product_id>/lessons/",
         UserLessons.as_view()),
]
