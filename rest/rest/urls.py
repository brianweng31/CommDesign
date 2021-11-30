from django.urls import path, re_path

#orig# from .views import EchoView
#add
from .views import FibView
from .views import LogView
#

urlpatterns = [
    #orig# re_path(r'^tutorial/?$', EchoView.as_view()),
    #add
    re_path(r'^fibonacci/?$', FibView.as_view()),
    re_path(r'^logs/?$', LogView.as_view()),
    #
]
