from django.urls import path

from homeapp.views import (
    HomePageView,
    TeamView,
    TariffsView,
    RabotaemView,
    PolnomochiyaView,
    TaynaView,
    SoglashenieView,
    VariantyView,
    PrivicyView,
    download_resume,
    cases_filter_view,
    PracticesView,
    PracticeDetailView,
    ServiceListView,
    ServiceDetailView,
    NewsListView,
    NewsDetailView,
    ReviewListView,
    ClientListView,
    ArticleListView,
    ArticleDetailView,
    VideoListView,
)

app_name = 'homeapp'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('team/', TeamView.as_view(), name='team'),
    path('tariffs/', TariffsView.as_view(), name='tariffs'),
    path('cases/', PracticesView.as_view(), name='cases'),

    # Procedure Pages
    path('kak-my-rabotaem/', RabotaemView.as_view(), name='rabotaem'),
    path('polnomochiya-advokata/', PolnomochiyaView.as_view(), name='polnomochiya'),
    path('advokatskaya-tayna/', TaynaView.as_view(), name='tayna'),
    path('soglashenie-i-order/', SoglashenieView.as_view(), name='soglashenie'),
    path('varianty-voznagrozhdeniya/', VariantyView.as_view(), name='varianty'),
    path('privicy/', PrivicyView.as_view(), name='privicy'),

    # Files
    path('download/<path:file_path>', download_resume, name='download'),

    # Services
    path("services/<str:audience>/", ServiceListView.as_view(), name="service_list"),
    path("services/detail/<slug:slug>/", ServiceDetailView.as_view(), name="service_detail"),

    # Practice
    path('practices/<int:pk>/', PracticeDetailView.as_view(), name='practice_detail'),
    path('cases/filter/', cases_filter_view, name='cases_filter'),

    # News
    path('news-list/', NewsListView.as_view(), name='news_list'),
    path('news_<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),

    # Reviews
    path('reviews/', ReviewListView.as_view(), name='reviews'),

    # Clients
    path("clients/", ClientListView.as_view(), name="client_list"),

    # Press Center
    path("press/articles/", ArticleListView.as_view(), name="article_list"),
    path("press/articles/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("press/videos/", VideoListView.as_view(), name="video_list"),
]
