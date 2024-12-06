# from django.db import models

# # Custom User Manager


# # Counter model that links to the User
# class Counter(models.Model):
#     # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="counter")
#     value = models.PositiveBigIntegerField(default=0)    

#     def __str__(self):
#         return f"CoinBalance: {self.value}"
# class Level(models.Model):
#     level = models.PositiveIntegerField(null=True, blank=True)
#     def __str__(self):
#         return f"level:{{self.level}}"

# class Mining(models.Model):
#     speed = models.PositiveIntegerField(default=3000, blank=True, null=True)
#     def __str__(self):
#         return f"Mining Spped:{self.speed} 4/hr"


# class Boost(models.Model):
#     boost_name = models.CharField(max_length=100, blank=True, null=True)
#     boost_value = models.PositiveIntegerField(blank=True, null=True)
#     needed_coin = models.PositiveIntegerField(blank=True, null=True)
#     level = models.CharField(blank=True, null=True, max_length=20, unique=True)

#     def __str__(self):
#         return f"Boost name:{self.boost_name} Boost value: {self.needed_coin}"
    
# # TaskList model
# class TaskList(models.Model):
#     Taskname = models.CharField(max_length=100)
#     Taskvalue = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"Task: {self.Taskname} - Value: {self.Taskvalue}"

# # users/models.py

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# # Custom User Manager
# class CustomUserManager(BaseUserManager):
  
#     def create_user(self, username, email, password=None):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email)
#         user.set_password(password)  # This automatically hashes the password
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None):
#         user = self.create_user(username, email, password)
#         user.is_admin = True  # Ensure the superuser has admin privileges
#         user.is_superuser = True  # Set superuser flag
#         user.is_staff = True  # Superusers must have staff status
#         user.save(using=self._db)
#         return user

# # Custom User model
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
    
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)  # Explicitly define is_superuser
#     is_staff = models.BooleanField(default=False)  # Make is_staff a regular field
#     # date_joined = models.DateTimeField(auto_now_add=True)

#     USERNAME_FIELD = 'email'  # Use email as the username
#     REQUIRED_FIELDS = ['username']  # Fields required for creating a superuser

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.username

### chat gpt ###

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Counter model that links to the User
class Counter(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="counter")
    value = models.PositiveBigIntegerField(default=0)    

    def __str__(self):
        return f"BALANCE: {self.value} \t \t USER={self.user}"

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
        return f"MINING SPEED: {self.speed} USER={self.user}"

# Boost model that links to the User
class Boost(models.Model):
    boost_name = models.CharField(max_length=100, blank=True, null=True)
    boost_value = models.PositiveIntegerField(blank=True, null=True)
    needed_coin = models.PositiveIntegerField(blank=True, null=True)
    level = models.CharField(blank=True, null=True, max_length=20, unique=False)
    assigned_users = models.ManyToManyField('CustomUser', related_name='boost')
    def __str__(self):
        return f"Boost name: {self.boost_name} | Boost value: {self.boost_value} | Needed coin: {self.needed_coin}"

# This model links users to the boosts they've used


# TaskList model that links to the User
class TaskList(models.Model):
    Taskname = models.CharField(max_length=100)
    Taskvalue = models.PositiveIntegerField(default=0)
    link = models.URLField(max_length=200, blank=True, null=True)
    assigned_users = models.ManyToManyField('CustomUser', related_name="tasks")

    def __str__(self):
        return f"Task: {self.Taskname} - Value: {self.Taskvalue}"



class UserSession(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
## invite logic.. you can you similar logic of the task list and boost 

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

## invite logic 

