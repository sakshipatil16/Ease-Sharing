"""
tt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from upload import views as upload_views
from django.conf import settings
from django.conf.urls.static import static
from ecommerce import views as ecommerce_views
from ecommerce.views import ItemDeleteView,  UserItemListView


urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', user_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html') ,name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('book/',upload_views.book_list,name='book_list'),
    path('book/upload',upload_views.upload_book,name='upload_book'),
    path('item/',ecommerce_views.item_list,name='item_list'),
    path('products/<int:pk>', ecommerce_views.ItemDetailView.as_view(template_name='product.html'),name='product'),
    path('item/upload',ecommerce_views.upload_item,name='upload_item'),
    path('item/<int:pk>/delete/',ItemDeleteView.as_view(template_name='item_confirm_delete.html'),name='item-delete'),
   path('add_to_cart/<int:pk>/',ecommerce_views.add_to_cart,name='add_to_cart'),
   path('remove_from_cart/<int:pk>/',ecommerce_views.remove_from_cart,name='remove_from_cart'),
   path('order-summary/',ecommerce_views.OrderSummaryView.as_view(),name='order-summary'),
    path('item/<int:pk>/comment/', ecommerce_views.add_comment_to_item, name='add_comment_to_item'),
    path('item/<int:pk>',UserItemListView.as_view(),name='user-items'),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
   