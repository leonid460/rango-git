from django.conf.urls import patterns, url
from rango import views

app_name = 'rango'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$',views.about, name='about'),
	url(r'^add_category/$', views.add_category, name='add_category'),

	url(r'^category/(?P<category_name_slug>[\w-]+)/add_page/$',
		 views.add_page, name='add_page'),
	
	url(r'^category/(?P<category_name_slug>[\w-]+)/$',
		views.show_category, name='show_category'),

	url(r'^restricted/', views.restricted, name='restricted'),

	url(r'^goto/', views.track_url, name='goto'),

	url(r'^add_profile/', views.register_profile, name='add_profile'),

	url(r'^profile/(?P<username>[\w-]+)/$', views.profile, name='profile'),

	url(r'^profiles_list/$', views.profiles_list, name='profiles_list'),

	# url(r'^register/$', views.register, name='register'),
	# url(r'^login/$', views.user_login, name='login'),
	# url(r'^logout/$', views.user_logout, name='logout'),
]