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
        path = settings.BASE_DIR / file.file.path.replace("/", "\\")
        print(path)
        # result = subprocess.run(['flake8', file.file.url], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # try:
        #     log = Logs.objects.get(file=file)
        #     log.text = result
        #     log.save()
        #
        # except Exception as ex:
        #     Logs.objects.create(file=file, text=result)
        #
        # file.status = FileStatuses.DONE
        # file.save()
        #
        # send_mail.delay(file.pk)


@shared_task()
def send_mail(pk):
    file_log = get_object_or_404(Logs, file=pk)

    send_mail(
        subject='Ваш файл проверен',
        message=file_log.text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=settings.EMAIL_HOST_USER
    )
