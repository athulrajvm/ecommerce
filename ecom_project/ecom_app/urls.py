from django.urls import path
from .import views

urlpatterns = [
   path("",views.home,name="home"),
   path("loginpage",views.loginpage,name="loginpage"),
   path("signuppage",views.signuppage,name="signuppage"),
   path("logfun",views.logfun,name="logfun"),
   path("usercreate",views.usercreate,name="usercreate"),
   path("adminhome",views.adminhome,name="adminhome"),
   path("customerhome",views.customerhome,name="customerhome"),
   path("add_category",views.add_category,name="add_category"),
   path("categoryfun",views.categoryfun,name="categoryfun"),
   path('category/<int:category_id>/', views.category_page, name='category_page'),
   path("add_product",views.add_product,name="add_product"),
   path("productfun",views.productfun,name="productfun"),
   path("view_product",views.view_product,name="view_product"),
   path("edit_product/<int:pk>",views.edit_product,name="edit_product"),
   path("editproduct/<int:p>",views.editproduct,name="editproduct"),
   path("delete_product/<int:p>",views.delete_product,name="delete_product"),
   path("view_user",views.view_user,name="view_user"),
   path("delete_user/<int:p>",views.delete_user,name="delete_user"),
   path("logoutfun",views.logoutfun,name="logoutfun"),
   path("edit_user/<int:p>",views.edit_user,name="edit_user"),
   path("edituser/<int:p>",views.edituser,name="edituser"),
   path("edituser",views.edituser,name="edituser"),
   path("user_update/<int:tr>",views.user_update,name="user_update"),
   path("aboutus",views.aboutus,name="aboutus"),
   path("menshoes",views.menshoes,name="menshoes"),
   path("womenshoes",views.womenshoes,name="womenshoes"),
   path("kidshoes",views.kidshoes,name="kidshoes"),
   path('product/<int:product_id>/', views.product_detail, name='product_detail'),
   path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
   path('cart/', views.cart_view, name='cart'),
   path('cart/update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
   path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
   path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
   path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
   path('cart/', views.cart_view, name='cart_view'),
   path('cart/', views.cart_view, name='cart'),
   

   

]



