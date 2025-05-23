from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_paid = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='tickets/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class EventRequest(models.Model):
    event_name = models.CharField(max_length=255)
    organizer_name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name
