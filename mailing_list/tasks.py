import os

import requests
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dotenv import load_dotenv

from solution_factory.celery import app

load_dotenv()
JWT_TOKEN = os.getenv('JWT_TOKEN')
MESSAGE_SERVICE_URL = os.getenv('MESSAGE_SERVICE_URL')


@app.task
def send_message(mail_id):
    """Method for sending a message to the client"""
    from mailing_list.models import Mail, StatusChoice

    message = get_object_or_404(Mail, id=mail_id)

    response = requests.post(
        url=f'{MESSAGE_SERVICE_URL}{message.id}',
        headers={
            'Authorization': f'Bearer {JWT_TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            'id': message.id,
            'phone': f'{message.client.operator_code}'
                     f'{message.client.phone_number}',
            'text': message.mailing_list.text
        }

    )
    if response.status_code == 200:
        message.status = StatusChoice.success.value
        message.sent_at = timezone.now()
    else:
        message.status = StatusChoice.failed.value
    message.save()


def cancel_task(mail_ids):
    """Method for canceling sending messages that have not yet been sent"""
    from mailing_list.models import Mail, StatusChoice

    task_name = 'mailing_list.tasks.send_message'
    scheduled_tasks = app.control.inspect().scheduled()
    for worker, tasks in scheduled_tasks.items():
        for task in tasks:
            if (
                task['request']['name'] == task_name
                    and task['request'].get('kwargs').get(
                    'mail_id'
                ) in mail_ids
            ):
                task_id = task['request']['id']
                app.control.revoke(
                    task_id=task_id, terminate=True, signal='SIGKILL'
                )
                message = get_object_or_404(
                    Mail, id=task['request'].get('kwargs').get('mail_id')
                )
                message.status = StatusChoice.canceled.value
                message.save()
