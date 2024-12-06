from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Counter model that links to the User
class Counter(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="counter")
    value = models.PositiveBigIntegerField(default=0)    

    def __str__(self):
        return f"CoinBalance: {self.value}"

# Level model that links to the User
class Level(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="level")
    level = models.PositiveIntegerField(null=True, blank=True, default=1)  # Default to level 1

    def __str__(self):
        return f"level: {self.level}"

# Mining model that links to the User
class Mining(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="mining")
    speed = models.PositiveIntegerField(default=3000, blank=True, null=True)  # Default mining speed

    def __str__(self):
        return f"Mining Speed: {self.speed} per hour"

# Boost model that links to the User
class Boost(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="boost")
    boost_name = models.CharField(max_length=100, blank=True, null=True)
    boost_value = models.PositiveIntegerField(blank=True, null=True)
    needed_coin = models.PositiveIntegerField(blank=True, null=True)
    level = models.CharField(blank=True, null=True, max_length=20, unique=True)

    def __str__(self):
        return f"Boost name: {self.boost_name} | Boost value: {self.boost_value} | Needed coin: {self.needed_coin}"

# TaskList model that links to the User
class TaskList(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="tasklist")
    Taskname = models.CharField(max_length=100)
    Taskvalue = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Task: {self.Taskname} - Value: {self.Taskvalue}"

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)

        # Create related models after user creation
        self._create_user_related_fields(user)

        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

    def _create_user_related_fields(self, user):
        # Create related models for Counter, Level, Mining, TaskList, and Boost
        Counter.objects.create(user=user)
        Mining.objects.create(user=user)
        Boost.objects.create(user=user)
        TaskList.objects.create(user=user)
        Level.objects.create(user=user)

# Custom User model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Fields required for creating a superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.username


<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" style="fill: rgba(5, 10, 109, 1);transform: ;msFilter:;"><path d="M21 5H3a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm-8 2h2v2h-2V7zm0 4h2v2h-2v-2zM9 7h2v2H9V7zm0 4h2v2H9v-2zM5 7h2v2H5V7zm0 4h2v2H5v-2zm12 6H7v-2h10v2zm2-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>