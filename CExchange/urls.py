from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('checkout/payment/', views.payment, name='payment'),
    path('add/' , views.add, name='add'),
    path('add/addrecord/', views.addrecord, name='addrecord'),
    path('profile/', views.profile, name='profile'),
    path('make_ex/', views.make_ex, name='make_ex'),
    path('make_ex/make_exchange/', views.make_exchange, name='make_exchange'),
    path('my_ex/', views.my_ex, name='my_ex'),
    path('ex_list/', views.ex_list, name='ex_list'),
    path('ex_list/confirm/<int:id>', views.confirm, name='confirm'),
    path('ex_list/confirm/deal/<int:id>', views.deal, name='deal'),
    path('fatality/', views.fatality, name='fatality'),
    path('success/', views.success, name='success'),
    path('complaint/', views.complaint, name='complaint'),
    path('complaint/addcomplaint/', views.addcomplaint, name='addcomplaint'),
    path('complaintlist/', views.complaintlist, name='complaintlist'),
    path('information/', views.information, name="information"),
    path('twoFA/', views.twoFA, name="twoFA"),
    path('twoFA/twoFALogin/', views.twoFALogin, name="twoFALogin"),
]