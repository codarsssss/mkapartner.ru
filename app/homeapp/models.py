from django.db import models
from django.db.models.query import QuerySet
from transliterate import slugify
from django.utils.safestring import mark_safe
from django.urls import reverse


def translit_filename(instance, filename):
    file_extension = filename.split(".")[-1]
    filename = slugify(instance.fio)
    return "resume/{}.{}".format(filename, file_extension)


class NewsPublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=News.Status.PUBLISHED)


# Модель новостей
class News(models.Model):
    class Status(models.TextChoices):
        NOT_PUBLISHED = "Нет", "Не опубликована"
        PUBLISHED = "Да", "Опубликована"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Слаг поста")
    text = models.TextField(verbose_name="Текст новости")
    status = models.CharField(
        verbose_name="Статус",
        max_length=3,
        choices=Status.choices,
        default=Status.NOT_PUBLISHED,
    )
    create_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    objects = models.Manager()  # Менеджер, применяемый по умолчанию
    published = NewsPublishedManager()  # Конкретно-прикладной менеджер

    class Meta:
        ordering = ["-create_datetime"]

        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=50, verbose_name="Фамилия Имя Отчество")
    min_context1 = models.TextField(verbose_name="Краткое описание для первой страницы")
    min_context2 = models.TextField(
        blank=True, verbose_name="Дополнительное поле короткого писания"
    )
    min_context3 = models.TextField(
        blank=True, verbose_name="Дополнительное поле короткого писания"
    )
    min_context4 = models.TextField(
        blank=True, verbose_name="Дополнительное поле короткого писания"
    )
    context = models.TextField(verbose_name="Полное описание")
    photo = models.ImageField(verbose_name="Фото", upload_to="partners/")
    time_create = models.DateTimeField(auto_now_add=True)
    my_order = models.IntegerField(
        blank=False,
        null=False,
        db_index=True,
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['my_order']
        verbose_name = "Партнера"
        verbose_name_plural = "Партнеры"

    def save(self, *args, **kwargs):
        if not self.my_order:
            super().save(*args, **kwargs)
            self.my_order = self.pk
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class PartnerPhoto(models.Model):
    partner = models.ForeignKey('Partner', related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='partner_photos/')
    caption = models.CharField(max_length=100, blank=True, verbose_name="Подпись к фото")

    def __str__(self):
        return f"Фото {self.partner.name}"


class PracticeCategory(models.Model):
    title = models.CharField(
        max_length=128, verbose_name="Наименование категории практики"
        )
    image = models.ImageField(
        verbose_name="Изображение", upload_to="practice_category/", blank=True, null=True
        )

    def __str__(self):        
        return f"{self.title}"

    class Meta:
        verbose_name = "категорию практики"
        verbose_name_plural = "Категории практики"

class PracticeInstance(models.Model):
    category = models.ForeignKey(
        PracticeCategory,
        on_delete=models.CASCADE,
        verbose_name="категория практики"
    )
    title = models.CharField(
        max_length=255, verbose_name="Название случая"
        )
    circumstances = models.TextField(
        verbose_name="Обстоятельства"
    )
    lawyer_position = models.TextField(
        verbose_name="Позиция адвоката"
    )
    outcome = models.TextField(
        verbose_name="Итог"
    )

    verdict_url = models.URLField(
        verbose_name="Ссылка на приговор",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Случай практики"
        verbose_name_plural = "Случаи практики"

    def __str__(self):
        return f"{self.title}"


class PracticeInstanceImage(models.Model):
    practice_instance = models.ForeignKey(
        PracticeInstance,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Случай практики"
    )
    image = models.ImageField(
        upload_to='practice_instance_images/',
        verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Изображение случая практики"
        verbose_name_plural = "Изображения случаев практики"

    def __str__(self):
        return f"Image for {self.practice_instance}"
