from django.conf.urls import patterns, url, include
from data.api import HeadTeacherResource
from tastypie.api import Api


# Setting the API base name and registering the API resources using
# Tastypies API function
api_resources = Api(api_name='api')
api_resources.register(HeadTeacherResource())
api_resources.prepend_urls()

# Setting the urlpatterns to hook into the api urls
urlpatterns = patterns('',
    url(r'^', include(api_resources.urls))
)
