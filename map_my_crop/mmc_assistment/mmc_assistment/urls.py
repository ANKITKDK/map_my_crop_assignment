from django.contrib import admin
from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Creating Router objects
router = DefaultRouter()

# Register StudentViewSet with Router
# router.register('sample/', views.SampleApi.as_view(), basename='student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userapi/', views.UserListCreateAPIView.as_view()),
    path('userapi/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),

    path('sample/', views.SampleApi.as_view()),

    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]
