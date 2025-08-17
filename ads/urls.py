from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    # Ad listing and details
    path('', views.ads_list_view, name='list'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('location/<slug:slug>/', views.location_view, name='location'),
    path('detail/<slug:slug>/', views.ad_detail_view, name='detail'),
    
    # Ad management
    path('create/', views.create_ad_view, name='create'),
    path('edit/<slug:slug>/', views.edit_ad_view, name='edit'),
    path('delete/<slug:slug>/', views.delete_ad_view, name='delete'),
    
    # AJAX endpoints
    path('report/', views.report_ad_view, name='report'),
    path('ajax-delete/', views.ajax_delete_ad, name='ajax_delete'),
]
