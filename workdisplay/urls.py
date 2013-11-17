from django.conf.urls import patterns, include, url
import base.views


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', base.views.home, name='home'),

   url(r'^admin/', include(admin.site.urls)),
)
