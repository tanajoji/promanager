from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.title
    
class EditorElement(models.Model):
    ELEMENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='elements')
    type = models.CharField(max_length=10, choices=ELEMENT_TYPES)
    text_content = models.TextField(blank=True)  # Only for text
    file = models.FileField(upload_to='editor_uploads/', blank=True, null=True)  # For images
    position_x = models.FloatField(default=0.5)
    position_y = models.FloatField(default=0.5)
    width = models.FloatField(default=50)
    height = models.FloatField(default=50)

    def __str__(self):
        return f"{self.type} element in {self.project.title}"