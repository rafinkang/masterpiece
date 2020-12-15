from django.db import models

# form 속성 정의
class test_frm(models.Model):
    post_message1 = models.CharField(max_length=25)
    post_message2 = models.EmailField()
    post_message3 = models.TextField(null=True)

# Create your models here.