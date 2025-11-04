from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


#USERS MANAGER
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo de email é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


#ROLES
class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    ONG = 'ONG', 'ONG'
    VOLUNTEER = 'VOLUNTEER', 'Voluntário'


#USER
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VOLUNTEER
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


#PROFILE - PERSON
class PersonProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='person_profile')
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    accept_announcements = models.BooleanField(default=False)

    def __str__(self):
        return self.name


#PROFILE - ONG
class OngProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='ong_profile')
    ong_name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.ong_name


#POST CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


#POST
class Post(models.Model):
    STATUS_CHOICES = [
        ('ABERTA', 'Aberta'),
        ('FECHADA', 'Fechada'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTA')
    ong = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


#POST CATEGORY N-N
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')


#COMMENTS 
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.post.title}"


#APPLICATIONS
class Application(models.Model):
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True, blank=True)  # Aceito / Rejeitado

    class Meta:
        unique_together = ('volunteer', 'post')

    def __str__(self):
        return f"{self.volunteer.username} → {self.post.title}"
