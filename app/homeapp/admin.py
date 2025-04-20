from django.contrib import admin
from django.contrib.admin import AdminSite
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline, SortableAdminBase

from .forms import NewsForm, PartnerForm
from .models import (
    News,
    Partner,
    PartnerPhoto,
    Review,
    PracticeCategory,
    PracticeInstance,
    PracticeInstanceImage,
    Service,
    ServiceBlock,
    ServiceCategory,
    Client,
    Video,
    Article,
)


class CustomAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Переопределяем порядок отображения приложений в админке
        """
        app_list = super().get_app_list(request)

        ordering = {
            'PracticeCategory': 1,
            'PracticeInstance': 2,
            'News': 3,
            'Partner': 4,
            'Worker': 5
        }

        # Сортируем модели внутри каждого приложения
        for app in app_list:
            app['models'].sort(key=lambda x: ordering.get(x['object_name'], 999))

        # Сортируем сами приложения
        app_list.sort(key=lambda x: ordering.get(x['models'][0]['object_name'], 999))

        return app_list


# экземпляр кастомной админки
custom_admin_site = CustomAdminSite(name='customadmin')


class NewsAdmin(admin.ModelAdmin):
    form = NewsForm
    list_display = ['title', 'slug', 'create_datetime', 'status']
    # Этот атрибут нужен для того, чтобы поле slug создавалось
    # автоматически. Работает только в админке!!!
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['status', 'create_datetime']
    search_fields = ['title', 'slug', 'text']
    ordering = ['status', '-create_datetime']
    readonly_fields = ['create_datetime']


# Создаём инлайн-редактирование для фотографий
class PartnerPhotoInline(admin.TabularInline):
    model = PartnerPhoto
    extra = 1  # Количество пустых форм для добавления новых фото
    fields = ['photo', 'caption']  # Указываем поля для редактирования


# Настройки для модели Partner в админке
class PartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = PartnerForm  # Подключаем кастомную форму
    list_display = ['name',]
    inlines = [PartnerPhotoInline]  # Добавляем инлайн-редактирование фотографий


class PracticeCategoryAdmin(admin.ModelAdmin):
    model = PracticeCategory
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)

class PracticeInstanceImageInline(admin.TabularInline):
    model = PracticeInstanceImage
    extra = 1  # Количество пустых форм для новых изображений

class PracticeInstanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category_title', 'partner')
    search_fields = ('title', 'circumstances', 'lawyer_position', 'outcome')
    list_filter = ('category__title', 'partner')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'partner')
        }),
        ('Details', {
            'fields': ('circumstances', 'lawyer_position', 'outcome', 'verdict_url')
        }),
    )
    inlines = [PracticeInstanceImageInline]

    def get_category_title(self, obj):
        return obj.category.title
    get_category_title.short_description = 'Категория практики'
    get_category_title.admin_order_field = 'category__title'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['author_name', 'content']


class ServiceBlockInline(SortableTabularInline):
    model = ServiceBlock
    extra = 1
    fields = ["type", "text", "image", "order"]
    ordering = ["order"]


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience')
    list_filter = ('audience',)
    search_fields = ('title',)


class ServiceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["title", "category", "is_active"]
    list_filter = ["category__audience", "category"]
    search_fields = ["title", "short_description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceBlockInline]


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'service']
    search_fields = ['name']
    list_filter = ['service']


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_active", "preview")
    readonly_fields = ("preview",)
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("-published_at",)
    fields = ("title", "url", "thumbnail", "preview", "published_at", "is_active")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_active")
    list_filter = ("is_active", "published_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    fields = ("title", "slug", "content", "published_at", "is_active")



custom_admin_site.register(PracticeCategory, PracticeCategoryAdmin)
custom_admin_site.register(PracticeInstance, PracticeInstanceAdmin)
custom_admin_site.register(News, NewsAdmin)
custom_admin_site.register(Partner, PartnerAdmin)
custom_admin_site.register(Review, ReviewAdmin)
custom_admin_site.register(Service, ServiceAdmin)
custom_admin_site.register(ServiceCategory, ServiceCategoryAdmin)
custom_admin_site.register(Client, ClientAdmin)
custom_admin_site.register(Video, VideoAdmin)
custom_admin_site.register(Article, ArticleAdmin)
