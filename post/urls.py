from rest_framework.routers import DefaultRouter

from post.views import TweetMediaViewSet, TweetViewSet

router = DefaultRouter()
router.register("tweet", TweetViewSet)
router.register('tweet_media', TweetMediaViewSet)

urlpatterns = router.urls
