from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Member(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Пользователь',
        related_name='membership')
    chat = models.ForeignKey(
        'core.Chat',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Чат',
        related_name='membership')
    last_read_message = models.ForeignKey(
        'core.Message',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Последнее прочитанное сообщение')

    class Meta:
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чатов'

    def __str__(self):
        return f"{self.user} at {self.chat}"


class Chat(models.Model):
    title = models.CharField(
        max_length=128,
        blank=False,
        default='Unnamed Chat', verbose_name='Название чата')
    members = models.ManyToManyField(User, through=Member, related_name='chat_members')
    host = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создатель чата')
    last_message = models.ForeignKey(
        'core.Message',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Последнее сообщение',
        related_name='+')

    def __str__(self):
        return f"{self.title}"


class Message(models.Model):
    class Meta:
        ordering = ('-sent_at',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    chat = models.ForeignKey(
        Chat,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Чат сообщения',
        related_name='messages_chat')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Отправитель')
    content = models.TextField(verbose_name='Содержимое')
    sent_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата отправки')

    def __str__(self):
        return '{} at {}'.format(self.content, self.sent_at)
