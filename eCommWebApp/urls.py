from django.urls import path
from eCommWebApp import views
from eCommWebApp.views import SimpleView
from django.views import View
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home2),
    path('home2/', views.home2),
    path('home3/', views.home3),
    # path('all', views.all),
    path('catfilter/<cv>', views.category_filter),
    path('range/', views.range),
    path('sort/<sv>', views.sort),
    path('registration/', views.registration),
    path('dummy/', views.dummyRegistration),
    path('login/', views.user_login),
    path('passwordreset', views.password_reset),
    path('logout/', views.user_logout),
    path('pd/<pid>', views.product_detail),
    path('addtocart/<pid>', views.addtocart),
    path('po/', views.place_order),
    path('cart/', views.cart),
    path('remove/<cid>', views.remove),
    path('removeitem/<oid>', views.removeFromPO),
    path('updateqty/<qv>/<cid>', views.updateqty),
    path('makepayment/', views.makepayment),
    path('sendmail/', views.send_user_mail),
    path('about/', views.about),
    path('contact/', views.contact),
    path('add/<a>/<b>', views.addition),
    path('myview/', SimpleView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)