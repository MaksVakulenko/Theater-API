from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Reservation


@receiver(post_save, sender=Reservation)
def send_booking_confirmation(sender, instance, created, **kwargs):
    if created:
        tickets = instance.tickets.all()
        performances = [ticket.performance for ticket in tickets]
        shows = [
            f"{performance.play.title} at {performance.show_time}"
            for performance in performances
        ]
        shows_str = ", ".join(shows)

        send_mail(
            "Booking Confirmation",
            f"Your booking for {shows_str} has been confirmed!",
            "theatre_api@gmail.com",
            [instance.user.email],
            fail_silently=False,
        )
