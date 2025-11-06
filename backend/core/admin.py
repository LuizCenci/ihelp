from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm


# USUÁRIOS PERSONALIZADOS
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        ('Informações de Login', {'fields': ('email', 'password')}),
        ('Dados Pessoais', {'fields': ('username', 'phone_number', 'country', 'state', 'city', 'role')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'country', 'state', 'city', 'role', 'password1', 'password2'),
        }),
    )


# PERFIS
@admin.register(PersonProfile)
class PersonProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'user', 'accept_announcements')
    search_fields = ('name', 'cpf', 'user__email')
    list_filter = ('accept_announcements',)


@admin.register(OngProfile)
class OngProfileAdmin(admin.ModelAdmin):
    list_display = ('ong_name', 'cnpj', 'user', 'is_approved')
    search_fields = ('ong_name', 'cnpj', 'user__email')
    list_filter = ('is_approved',)


# CATEGORIAS
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# POSTS
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(PostAnnouncement)
class PostAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'ong', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description', 'ong__email')
    inlines = [PostCategoryInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'photo', 'status', 'ong')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


# ============================================
# ADMIN: PostFeed
# ============================================
@admin.register(PostFeed)
class PostFeedAdmin(admin.ModelAdmin):
    list_display = ('ong', 'created_at')
    search_fields = ('description', 'ong__email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('description', 'photo', 'ong')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


# COMENTÁRIOS
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('content', 'user__email', 'post__title')
    date_hierarchy = 'created_at'


# CANDIDATURAS
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'post', 'application_date', 'status')
    search_fields = ('volunteer__email', 'post__title')
    list_filter = ('status',)
    date_hierarchy = 'application_date'
