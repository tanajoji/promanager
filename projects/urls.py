from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add_project, name='add_project'),
    path('delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('update-title/<int:pk>/', views.update_project_title, name='update_project_title'),
    path('edit/<int:pk>/', views.project_editor, name='edit_project'),
    path('<int:pk>/add_text/', views.add_text_element, name='add_text_element'),
    path('<int:pk>/upload/', views.upload_editor_file, name='upload_editor_file'),
    path('update-element-properties/<int:element_id>/', views.update_element_properties, name='update_element_properties'),
    path('delete-element/<int:element_id>/', views.delete_editor_element, name='delete_editor_element'),
    path('copy-element/<int:element_id>/', views.copy_editor_element, name='copy_editor_element'),
    path('add-viewer/<int:pk>/', views.add_viewer, name='add_viewer'),
]