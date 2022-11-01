from rest_framework.routers import DefaultRouter

from post.views import TweetViewSet

router = DefaultRouter()
router.register("tweet", TweetViewSet)

urlpatterns = router.urls
