from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('add_site', views.add_site, name='add-site'),
    path('list_sites', views.list_sites, name='list-sites'),
    path('show_site/<site_id>', views.show_site, name='show-site'),
    path('search_sites', views.search_sites, name='search-sites'),
    path('update_site/<site_id>', views.update_site, name='update-site'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('add_event', views.add_event, name='add-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_site/<site_id>', views.delete_site, name='delete-site'),
    path('site_text', views.site_text, name='site_text'),
    path('site_csv', views.site_csv, name='site_csv'),
    path('site_pdf', views.site_pdf, name='site_pdf'),
    path('my_events', views.my_events, name='my_events'),
    path('search_events', views.search_events, name='search_events'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('site_events/<site_id>', views.site_events, name='site-events'),
    path('show_event/<event_id>', views.show_event, name='show-event'),
]
