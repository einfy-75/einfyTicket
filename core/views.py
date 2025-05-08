from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event, Ticket
from .serializers import EventRequestSerializer, EventSerializer, TicketSerializer
from django.shortcuts import get_object_or_404
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import base64

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@api_view(['POST'])
def book_ticket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save(is_paid=False)  # Wait for payment before marking as paid
        return Response({
            "message": "Ticket booked. Awaiting payment confirmation.",
            "ticket_id": ticket.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_payment(request):
    ticket_id = request.data.get("ticket_id")
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.is_paid:
        return Response({"message": "Ticket already confirmed."})

    # Mark as paid
    ticket.is_paid = True

    # Generate QR code
    qr = qrcode.make(f"{ticket.id}-{ticket.email}")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    file_name = f"ticket_{ticket.id}.png"
    ticket.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=True)

    ticket.save()
    return Response({"message": "Payment confirmed. QR code generated."})


@api_view(['POST'])
def verify_ticket(request):
    ticket_id = request.data.get("ticket_id")
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not ticket.is_paid:
        return Response({"status": "unpaid"}, status=400)

    if ticket.is_used:
        return Response({"status": "already_used"}, status=400)

    ticket.is_used = True
    ticket.save()
    return Response({
        "status": "valid",
        "name": ticket.name,
        "event": ticket.event.title
    })
@api_view(['POST'])
def submit_event_request(request):
    serializer = EventRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Event request submitted. Await admin approval."}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def simulate_payment(request):
    ticket_id = request.data.get('ticket_id')

    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=404)

    if ticket.is_paid:
        return Response({'detail': 'Ticket already paid'}, status=200)

    ticket.is_paid = True

    # Generate QR code
    qr = qrcode.make(f"{ticket.id}-{ticket.email}")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    filename = f"ticket_{ticket.id}.png"
    ticket.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

    ticket.save()
    return Response({'detail': 'Payment simulated. Ticket is now confirmed and QR code generated.'})
