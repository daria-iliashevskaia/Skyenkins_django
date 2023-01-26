from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import User


class FileStatuses:

    NEW = "new"
    DONE = "done"
    PROCESSED = "processed"
    UPDATE = "update"

    STATUS = [(NEW, "new"), (DONE, "done"), (PROCESSED, "processed"), (UPDATE, "update")]


class File(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название')

    owner = models.ForeignKey(User,
                              null=True,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец')

    file = models.FileField(upload_to='files/',
                            validators=[FileExtensionValidator(allowed_extensions=["py"])],
                            verbose_name='Файл')

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      verbose_name='Дата создания')

    status = models.CharField(max_length=100,
                              choices=FileStatuses.STATUS,
                              default=FileStatuses.NEW,
                              verbose_name='Статус')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['status']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super().delete(*args, **kwargs)
        storage.delete(path)


class Logs(models.Model):

    file = models.ForeignKey(File,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='Файл')

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      verbose_name='Дата создания')

    text = models.TextField(verbose_name='Текст')
    send_mail = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['created_at']

    def __str__(self):
        return self.text
