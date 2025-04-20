from django.urls import path
from homeapp.views import (
    home_index,
    tariffs_view,
    team_view,
    practices_view,
    rabotaem_view,
    polnomochiya_view,
    tayna_view,
    soglashenie_view,
    varianty_view,
    privicy_view,
    download_resume,
    get_news_list,
    news_detail,
    PracticeDetailView,
    ReviewListView,
    cases_filter_view,
    service_list_view,
    service_detail_view,
    client_list_view,
)


app_name = 'homeapp'
urlpatterns = [
    path('', home_index, name='index'),
    path('tariffs/', tariffs_view, name='tariffs'),
    path('team/', team_view, name='team'),
    path('cases/', practices_view, name='cases'),
    path('kak-my-rabotaem/', rabotaem_view, name='rabotaem'),
    path('polnomochiya-advokata/', polnomochiya_view, name='polnomochiya'),
    path('advokatskaya-tayna/', tayna_view, name='tayna'),
    path('soglashenie-i-order/', soglashenie_view, name='soglashenie'),
    path('varianty-voznagrozhdeniya/', varianty_view, name='varianty'),
    path('privicy/', privicy_view, name='privicy'),
    path('download/<path:file_path>', download_resume, name='download'),
    path("services/<str:audience>/", service_list_view, name="service_list"),
    path("services/detail/<slug:slug>/", service_detail_view, name="service_detail"),
    path('news-list/', get_news_list, name='news_list'),
    path('news_<slug:slug>/', news_detail, name='news_detail'),
    path('practices/<int:pk>/', PracticeDetailView.as_view(), name='practice_detail'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('cases/filter/', cases_filter_view, name='cases_filter'),
    path("clients/", client_list_view, name="client_list"),

]
