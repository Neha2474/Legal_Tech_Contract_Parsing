from django.urls import path
from . import views
from .views import DocumentUploadView, upload_document

urlpatterns = [
    path("", upload_document, name="upload-page"),
    path("api/upload/", DocumentUploadView.as_view(), name="api-upload"),
    path(
        "document/<int:document_id>/",
        views.document_detail,
        name="document_detail"
    ),
]