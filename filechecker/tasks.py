from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from Skyenkins_django import settings
from filechecker.models import File, Logs, FileStatuses
import subprocess
from Skyenkins_django.celery import app
from django.conf import settings


@app.task
def file_check():

    file_list = File.objects.filter(status__in=["new", "update"])

    for file in file_list:

        result = subprocess.run(['flake8', file.file.path], stdout=subprocess.PIPE).stdout.decode('utf-8')
        try:
            log = Logs.objects.get(file=file)
            log.text = result
            log.save()

        except Exception as ex:
            Logs.objects.create(file=file, text=result)

        file.status = FileStatuses.DONE
        file.save()

        send_email.delay(file.pk)


@shared_task()
def send_email(pk):
    log = Logs.objects.get(file_id=pk)
    log.send_mail = 1
    log.save()

    send_mail(
        subject='Ваш файл проверен',
        message=log.text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[log.file.owner.email]
    )

