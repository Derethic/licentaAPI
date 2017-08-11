from django.conf.urls import url

from ads.views import UserList, CustomObtainAuthToken, UserDetail, RegisterView, CategoryView, AdView, AdDetail, \
    UserAdList, ReceivedMessageList, SentMessageList, ConversationList, CreateMessageView

urlpatterns = [

    # Routes for login,register and users
    url(r'^login/$', CustomObtainAuthToken.as_view()),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),

    # Routes for ad categories
    url(r'^categories/$', CategoryView.as_view()),

    # Routes for ads
    url(r'^ads/$', AdView.as_view()),
    url(r'^ad/(?P<pk>[0-9]+)/$', AdDetail.as_view()),
    url(r'^user/ads/$', UserAdList.as_view()),

    # Routes for messages
    url(r'^user/messages/received/$', ReceivedMessageList.as_view()),
    url(r'^user/messages/sent/$', SentMessageList.as_view()),
    url(r'^user/conversation/(?P<pk>[0-9]+)/$', ConversationList.as_view()),
    url(r'^create/message/$', CreateMessageView.as_view()),

]
