from io import BytesIO
from django.contrib import admin
from django.core.files.base import ContentFile
import qrcode

from .models import Event, Ticket, EventRequest

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'venue', 'price']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['event', 'name', 'email', 'is_paid', 'is_used', 'created_at']
    list_filter = ['is_paid', 'is_used', 'event']
    actions = ['mark_as_paid']

    @admin.action(description='Mark selected tickets as paid and generate QR codes')
    def mark_as_paid(self, request, queryset):
        for ticket in queryset:
            if not ticket.is_paid:
                ticket.is_paid = True
                qr = qrcode.make(f"{ticket.id}-{ticket.email}")
                buffer = BytesIO()
                qr.save(buffer, format="PNG")
                filename = f"ticket_{ticket.id}.png"
                ticket.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)
                ticket.save()

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'organizer_name', 'email', 'is_approved']
    list_filter = ['is_approved', 'submitted_at']
