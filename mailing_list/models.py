from enum import Enum

import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from pytz import all_timezones

from mailing_list.constants import SHOWN_LENGTH
from mailing_list.tasks import send_message


class StatusChoice(Enum):
    success = 'Success'
    failed = 'Failed'
    pending = 'Pending'
    canceled = 'Canceled'


class Client(models.Model):
    """Model for Client objects"""
    TIMEZONES = tuple(zip(all_timezones, all_timezones))
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^7\d{10}$',
                message='Incorrect phone format',
            ),
        ]
    )
    operator_code = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^\d{2,5}$',
                message='Incorrect operator code format',
            ),
        ]
    )
    tag = models.CharField(max_length=50)
    time_zone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default='UTC'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'Client №{self.id} / ({self.operator_code}){self.phone_number}'
        )


class MailingList(models.Model):
    """Model for MailingList objects"""
    run_date = models.DateTimeField(
        verbose_name='Run date',
    )
    text = models.TextField(
        verbose_name='Text',
    )
    client_filter = models.JSONField(
        null=True
    )
    end_date = models.DateTimeField(
        verbose_name='End date',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'Mail list №{self.id} / Run date: {self.run_date} \n'
            f' {self.text[:SHOWN_LENGTH]} / End date: {self.end_date}'
        )

    def start_sending(self):
        """Method to send message to Clients"""
        current_time = timezone.now()
        clients = Client.objects.filter(**self.client_filter)
        for client in clients:
            client_timezone = pytz.timezone(client.time_zone)
            run_date_client = client_timezone.localize(
                self.run_date.replace(tzinfo=None)
            )
            end_date_client = client_timezone.localize(
                self.end_date.replace(tzinfo=None)
            )
            message = Mail.objects.create(
                mailing_list_id=self.id,
                client_id=client.id,
            )
            if run_date_client <= current_time <= end_date_client:
                send_message.apply_async(
                    kwargs={
                        'mail_id': message.id,
                    },
                )
            elif current_time < run_date_client < end_date_client:
                send_message.apply_async(
                    kwargs={
                        'mail_id': message.id,
                    },
                    eta=run_date_client,
                    expires=end_date_client,
                )


class Mail(models.Model):
    """Model for Mail objects"""
    sent_at = models.DateTimeField(
        verbose_name='Sent date',
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=[(status.name, status.value) for status in StatusChoice],
        default=StatusChoice.pending.value
    )
    mailing_list = models.ForeignKey(
        MailingList,
        null=True,
        on_delete=models.SET_NULL,
        related_name='mailing_list',
        verbose_name='Mailing list',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='client',
        verbose_name='Client',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'Client №{self.client.id} / Status: {self.status} \n'
            f' Mail №{self.id} / {self.mailing_list.text[:SHOWN_LENGTH]}'
        )
