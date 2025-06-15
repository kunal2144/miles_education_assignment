from django.urls import path
from .views import UserActivityLogView

urlpatterns = [
    path('', UserActivityLogView.as_view(), name='logs-list-create'),
    path('<int:pk>/', UserActivityLogView.as_view(), name='logs-detail-update'),
]
