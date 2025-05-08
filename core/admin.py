from io import BytesIO
from django.contrib import admin
import qrcode
from .models import Event, Ticket
from .models import EventRequest

admin.site.register(Event)
admin.site.register(Ticket)


@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'organizer_name', 'email', 'is_approved']
    list_filter = ['is_approved', 'submitted_at']

@admin.action(description='Mark as paid and generate QR')
def mark_as_paid(self, request, queryset):
    for ticket in queryset:
        if not ticket.is_paid:
            ticket.is_paid = True
            qr = qrcode.make(f"{ticket.id}-{ticket.email}")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            filename = f"ticket_{ticket.id}.png"
            ticket.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True) # type: ignore
            ticket.save()
