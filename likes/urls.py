from django.urls import path, include

from likes.views import *

app_name = 'likes'

urlpatterns = [
    path('likes/', include([
        path('add/', AddLikeView.as_view(), name='add'),
        path('remove/', RemoveLikeView.as_view(), name='remove'),
    ]))
]