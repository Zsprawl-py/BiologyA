from django.urls import path, include
from . import views

# app_name = 'courses'

urlpatterns = [
    ## manage
    path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    # courses urls
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/edit', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    # module
    path('<int:pk>/module', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    # content
    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='module_content_delete'),
    path('module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list'),

    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('', views.CourseListView.as_view(), name='course_list'),
]