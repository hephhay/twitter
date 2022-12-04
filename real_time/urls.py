from rest_framework.routers import DefaultRouter

from real_time.views import GroupViewSet, MessageViewSet, NotficationViewSet

router = DefaultRouter()

router.register('groups', GroupViewSet)
router.register('messages', MessageViewSet)
router.register('Notification', NotficationViewSet)

urlpatterns = router.urls
