from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, user_name, password):
        if not email:
            raise ValueError('Users must have an email address / 이메일 주소는 필수 항목입니다.')

        user = self.model(
            email=self.normalize_email(email),
            user_name = user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password):
        user = self.create_user(
            email=email,
            user_name = user_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser =True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    # 테스팅을 위해 일단 True
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('user_name',)

    def __str__(self):
        return self.user_name
    
    class Meta:
        db_table = 'User'

