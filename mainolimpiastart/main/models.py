from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from .services.utils import unique_slugify


class Notifications(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    description_footer = models.TextField(blank=True, verbose_name="Дополнительное описание")

    class Meta:
        db_table = 'app_notifications'
        verbose_name = 'Уведомления'
        verbose_name_plural = 'Уведомления'


class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name="Заголовок")

    class Meta:
        db_table = 'app_team'
        verbose_name = 'Наименование команды'
        verbose_name_plural = 'Наименование команды'

    def __str__(self):
        return f'{self.name}'


class Tutor(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя и фамилия тренера")

    class Meta:
        db_table = 'app_tutor'
        verbose_name = 'Тренеры'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return f'/tutor/'


class Location(models.Model):
    location_name = models.CharField(max_length=255, verbose_name="Локация")

    class Meta:
        db_table = 'app_location'
        verbose_name = 'Локация'
        verbose_name_plural = 'Локация'

    def __str__(self):
        return f'{self.location_name}'

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return f'/location/'


class Schedule(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    date_training = models.DateField(verbose_name="Дата тренировки")
    start_training = models.TimeField(verbose_name="Начало тренировки")
    finish_training = models.TimeField(verbose_name="Конец тренировки")
    location_name = models.OneToOneField(Location, on_delete=models.CASCADE, verbose_name="Локация")
    tutor = models.OneToOneField(Tutor, on_delete=models.CASCADE, verbose_name="Тренер")

    class Meta:
        db_table = 'app_schedule'
        ordering = ('team',)
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        """
        Возвращение строки
        """
        return self.team.name

    def get_absolute_url(self):
        """
        Ссылка на расписание
        """
        return reverse('team_id', kwargs={'schedule_id': self.slug})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    phone = PhoneNumberField(verbose_name="Номер телефона")
    photo = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.jpg',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])

    class Meta:
        db_table = 'app_profiles'
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('profile_detail', kwargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Documents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    files = models.FileField(
        verbose_name='Страховка',
        upload_to='documents/insurance/%Y/%m/%d/',
        default='documents/insurance/default.pdf',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])])

    class Meta:
        db_table = 'app_documents'
        ordering = ('user',)
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return f'/documents/'


class DateTime(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата и время")

    class Meta:
        db_table = 'app_datetime'
        verbose_name = 'Дата и время индивидувльного занятия'
        verbose_name_plural = 'Дата и время индивидувльного занятия'

    def __str__(self):
        return f'{self.datetime}'

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return f'/datetime/'


class Indiv(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    tutor = models.OneToOneField(Tutor, on_delete=models.CASCADE, verbose_name="Тренер")
    child_name = models.CharField(max_length=255, verbose_name="Имя и фамилия ребенка")
    datetime = models.OneToOneField(DateTime, on_delete=models.CASCADE, verbose_name="Дата и время индивидуального занятия")
    location_name = models.OneToOneField(Location, on_delete=models.CASCADE, verbose_name="Локация")

    class Meta:
        db_table = 'app_indiv'
        ordering = ('user',)
        verbose_name = 'Запись на индивидуальные занятия'
        verbose_name_plural = 'Запись на индивидуальные занятия'

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return f'/indiv/'


class News(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    name = models.CharField(max_length=255, verbose_name="Имя и фамилия тренера")
    photo = models.ImageField(
        verbose_name='Фото тренера',
        upload_to='images/news/tutor/%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])

    class Meta:
        db_table = 'app_news'
        ordering = ('user',)
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('news', kwargs={'news_id': self.slug})


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        verbose_name='Новости',
        upload_to='images/news/%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])

    class Meta:
        db_table = 'app_news_image'
        verbose_name = 'Фото для новостей'
        verbose_name_plural = 'Фото для новостей'

    def __str__(self):
        return f'{self.image}'
