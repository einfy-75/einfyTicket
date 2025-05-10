from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, book_ticket, confirm_payment, simulate_payment, verify_ticket
from .views import submit_event_request
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),  
    path('submit-event/', submit_event_request, name='submit-event'),
    path('book-ticket/', book_ticket, name='book-ticket'),
    path('confirm-payment/', confirm_payment, name='confirm-payment'),
    path('verify-ticket/', verify_ticket, name='verify-ticket'),
    path('simulate-payment/', simulate_payment, name='simulate-payment'),
]