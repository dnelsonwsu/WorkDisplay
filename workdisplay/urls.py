from django.conf.urls import patterns, include, url
import base.views


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', base.views.home, name='home'),
   url(r'^ajax_poll', base.views.ajax_poll, name='calendar'),

   url(r'^admin/', include(admin.site.urls)),
)
