from tkinter import CASCADE
from wsgiref.validate import validator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinLengthValidator



# Create your models here.

# photo 에 쌓이는 폴더를 지정하지 않으면...설정된 media folder에 쌓이게 됨
# upload_to 옵션 (function 입력도 가능, UUID)
# dir 지정가능하고, 날짜 option 으로 dirtory를 나눌 수 있음 파일 다시 올릴 때 반영됨
# 파일 삭제 logic은 별도로 만들어야 함(참조 없는 파일 삭제 등..)

# from django.contrib.auth.models import User
# 바뀌는/update 되는 거라 아래처럼하면 좋지 않음
# settings.AUTH_USER_MODEL =>를 만들어 사용하는 것이 좋음



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(
        validators=[MinLengthValidator(10)]
    )
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y/%m/%d')
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag_set = models.ManyToManyField('Tag', blank=True)
 

    # Java의 toString
    def __str__(self):
        # return f"Custom Post object ({self.id})"
        return self.message

    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])

    class Meta:
        ordering = ['-id']
        
    


    # def message_length(self):
    #     return len(self.message)        
    # message_length.short_description ="msg 글자수"
    
    
    


##################################
#  UUID를 통한 파일명 정하기 
##################################
# import os
# from uuid import uuid4
# from django.utils import timezone

# def uuid_name_upload_to(instance, filename):
#     app_label = instance.__class__._meta.app_label     # 앱 별로
#     cls_name = instance.__class__.__name__.lower()      # 모델 별로
#     ymd_path = timezone.now().strftime('%Y/%m/%d')      # 날짜 별로
#     uuid_name = uuid4().hex
#     extension = os.path.splitext(filename)[-1].lower()  #확장자 추출, 소문자 변환
#     return '/'.join([
#         app_label,
#         cls_name,
#         ymd_path,
#         uuid_name[:2],
#         uuid_name + extension,
#     ])


class Comment(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE)    #post_id 라는 field 생성됨
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # post_set = models.ManyToManyField(Post)
    
    def __str__(self):
        return self.name