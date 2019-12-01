from django.urls import path
#from django.conf.urls import patterns, url
from rango import views

app_name = 'rango'
urlpatterns = [
	path('', views.index, name='index'),
	path('about/',views.about, name='about'),
	path('add_category/', views.add_category, name='add_category'),

	path('category/<category_name_slug>/add_page/',
		 views.add_page, name='add_page'),
	
	path('category/<category_name_slug>',
		views.show_category, name='show_category'),

	path('restricted/', views.restricted, name='restricted'),

	path('goto/', views.track_url, name='goto'),

	path('add_profile/', views.register_profile, name='add_profile'),

	path('profile/<username>', views.profile, name='profile'),

	path('profiles_list', views.profiles_list, name='profiles_list'),

	# url(r'^register/$', views.register, name='register'),
	# url(r'^login/$', views.user_login, name='login'),
	# url(r'^logout/$', views.user_logout, name='logout'),
]
