from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, book_ticket, confirm_payment, simulate_payment, verify_ticket
from .views import submit_event_request
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('book/', book_ticket),
    path('confirm-payment/', confirm_payment),
    path('verify/', verify_ticket),
    path('submit-event-request/', submit_event_request),
    path('simulate-payment/', simulate_payment),
]

