from django.urls import path
from address.views import AddressView


urlpatterns = [
  path('address/', AddressView.as_view()),
  path('address/<str:address_id>/', AddressView.as_view()),
]