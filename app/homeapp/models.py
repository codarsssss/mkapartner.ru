import re
from django.db import models
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.urls import reverse
from transliterate import slugify
from ckeditor.fields import RichTextField


def translit_filename(instance, filename):
    file_extension = filename.split(".")[-1]
    filename = slugify(instance.fio)
    return f"resume/{filename}.{file_extension}"


class NewsPublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=News.Status.PUBLISHED)


class News(models.Model):
    class Status(models.TextChoices):
        NOT_PUBLISHED = "Нет", "Не опубликована"
        PUBLISHED = "Да", "Опубликована"

    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Слаг поста")
    text = RichTextField("Текст новости")
    video_link = models.URLField("Видео", blank=True)
    status = models.CharField("Статус", max_length=3, choices=Status.choices, default=Status.NOT_PUBLISHED)
    create_datetime = models.DateTimeField("Дата создания", auto_now_add=True)

    objects = models.Manager()
    published = NewsPublishedManager()

    class Meta:
        ordering = ["-create_datetime"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("homeapp:news_detail", args=[self.slug])


class Partner(models.Model):
    name = models.CharField("Фамилия Имя Отчество", max_length=50)
    min_context1 = models.TextField("Краткое описание для первой страницы")
    min_context2 = models.TextField("Доп. поле 1", blank=True)
    min_context3 = models.TextField("Доп. поле 2", blank=True)
    min_context4 = models.TextField("Доп. поле 3", blank=True)
    context = models.TextField("Полное описание")
    photo = models.ImageField("Фото", upload_to="partners/")
    time_create = models.DateTimeField(auto_now_add=True)
    my_order = models.IntegerField("Порядок", db_index=True)

    class Meta:
        ordering = ['my_order']
        verbose_name = "Партнера"
        verbose_name_plural = "Партнеры"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.my_order:
            self.my_order = self.pk
            super().save(update_fields=["my_order"])

    def __str__(self):
        return self.name


class PartnerPhoto(models.Model):
    partner = models.ForeignKey(Partner, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='partner_photos/')
    caption = models.CharField("Подпись к фото", max_length=100, blank=True)

    def __str__(self):
        return f"Фото для {self.partner.name}"


class PracticeCategory(models.Model):
    title = models.CharField("Наименование категории практики", max_length=128)
    image = models.ImageField("Изображение", upload_to="practice_category/", blank=True, null=True)

    class Meta:
        verbose_name = "категорию практики"
        verbose_name_plural = "Категории практики"

    def __str__(self):
        return self.title


class PracticeInstance(models.Model):
    category = models.ForeignKey(PracticeCategory, on_delete=models.CASCADE, verbose_name="Категория практики")
    title = models.CharField("Название случая", max_length=255)
    circumstances = models.TextField("Обстоятельства")
    lawyer_position = models.TextField("Позиция адвоката")
    outcome = models.TextField("Итог")
    verdict_url = models.URLField("Ссылка на приговор", blank=True, null=True)
    partner = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='practice', verbose_name='Адвокат')

    class Meta:
        verbose_name = "Случай практики"
        verbose_name_plural = "Случаи практики"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('homeapp:practice_detail', args=[self.pk])


class PracticeInstanceImage(models.Model):
    practice_instance = models.ForeignKey(PracticeInstance, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField("Изображение", upload_to='practice_instance_images/')

    class Meta:
        verbose_name = "Изображение случая практики"
        verbose_name_plural = "Изображения случаев практики"

    def __str__(self):
        return f"Изображение: {self.practice_instance.title}"


class Review(models.Model):
    author_name = models.CharField("Имя клиента", max_length=100)
    content = models.TextField("Текст отзыва")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    is_active = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.author_name}: {self.content[:30]}..."


class ServiceCategory(models.Model):
    class Audience(models.TextChoices):
        LEGAL = "legal", "Юридические лица"
        INDIVIDUAL = "individual", "Физические лица"

    title = models.CharField("Название категории", max_length=255)
    description = models.TextField("Описание", blank=True)
    audience = models.CharField("Тип клиента", max_length=20, choices=Audience.choices, default=Audience.INDIVIDUAL)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"
        ordering = ['order']

    def __str__(self):
        return self.title


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services", verbose_name="Категория")
    title = models.CharField("Название услуги", max_length=255)
    slug = models.SlugField("Слаг", unique=True)
    short_description = models.TextField("Краткое описание", blank=True)
    image = models.ImageField("Обложка", upload_to="services/", blank=True, null=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title


class ServiceBlock(models.Model):
    class BlockType(models.TextChoices):
        TITLE = "title", "Заголовок"
        TEXT = "text", "Текст"
        IMAGE = "image", "Изображение"
        LIST = "list", "Список"
        QUOTE = "quote", "Цитата"
        HTML = "html", "HTML (сырой код)"

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="blocks", verbose_name="Услуга")
    type = models.CharField("Тип блока", max_length=20, choices=BlockType.choices, default=BlockType.TEXT)
    order = models.PositiveIntegerField("Порядок", default=0)
    text = models.TextField("Текст", blank=True)
    image = models.ImageField("Изображение", upload_to="services/blocks/", blank=True, null=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Блок услуги"
        verbose_name_plural = "Блоки услуги"

    def __str__(self):
        return f"{self.get_type_display()} — {self.service.title}"


class Client(models.Model):
    name = models.CharField("Название клиента", max_length=255)
    logo = models.ImageField("Логотип", upload_to="clients/", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип услуги")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    url = models.URLField("Ссылка на видео")
    published_at = models.DateField("Дата публикации")
    thumbnail = models.ImageField("Превью", upload_to="videos/", blank=True, null=True)
    is_active = models.BooleanField("Активно", default=True)
    practice = models.ForeignKey("PracticeInstance", on_delete=models.SET_NULL, related_name="videos",
                                 verbose_name="Случай практики", null=True, blank=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.title

    @property
    def youtube_id(self):
        """
        Возвращает ID видео с YouTube, извлекая его из ссылки.

        Поддерживаются ссылки формата:
        - https://youtu.be/XYZ
        - https://www.youtube.com/watch?v=XYZ

        Returns:
            str: Идентификатор видео на YouTube или пустая строка, если не найден.
        """
        if "youtu.be" in self.url:
            return self.url.split("/")[-1]
        if "youtube.com/watch?v=" in self.url:
            return self.url.split("v=")[-1].split("&")[0]
        return ""

    @property
    def rutube_embed_url(self):
        """
        Возвращает embed-ссылку для RuTube, если ссылка является валидной.

        Пример исходной ссылки:
        - https://rutube.ru/video/UUID/

        Returns:
            str: Ссылка для вставки видео с RuTube или пустая строка, если не распознано.
        """
        match = re.search(r"rutube\.ru/video/([a-zA-Z0-9]+)/?", self.url)
        if match:
            return f"https://rutube.ru/play/embed/{match.group(1)}"
        return ""

    @property
    def youtube_thumbnail(self):
        """
        Формирует ссылку на превью YouTube (кадр из видео).

        Используется, если вручную не загружено изображение-превью.

        Returns:
            str: URL на превью изображения с YouTube.
        """
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"

    def preview(self):
        """
        Возвращает HTML-превью для отображения в админке.

        Если загружено кастомное превью — используется оно.
        Если видео с YouTube — используется превью с YouTube.
        Если видео с RuTube — отображается заглушка.
        Иначе — "-".

        Returns:
            str: HTML-разметка превью.
        """
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" style="height: 100px;">')
        elif "youtube.com" in self.url or "youtu.be" in self.url:
            return mark_safe(
                f'<img src="https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg" style="height: 100px;">')
        elif "rutube.ru" in self.url and self.rutube_embed_url:
            return mark_safe('<span style="color: #999;">Превью не доступно</span>')
        return "-"

    preview.short_description = "Превью"


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Слаг", unique=True)
    content = RichTextField("Текст статьи")
    published_at = models.DateField("Дата публикации")
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("homeapp:article_detail", args=[self.slug])
