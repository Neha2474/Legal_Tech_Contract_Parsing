from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='contracts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    # Risk analysis results
    risk_score = models.IntegerField(default=0)
    risk_level = models.CharField(
        max_length=20,
        default="Not analyzed"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title