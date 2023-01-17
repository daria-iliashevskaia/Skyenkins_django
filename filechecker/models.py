from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import User


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

    is_checked = models.BooleanField(default=False,
                                     verbose_name='Проверено')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['is_checked']

    def __str__(self):
        return self.name


class Logs(models.Model):

    file = models.ForeignKey(File,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='Файл')

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      verbose_name='Дата создания')

    text = models.CharField(max_length=800, verbose_name='Текст')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['created_at']

    def __str__(self):
        return self.text
