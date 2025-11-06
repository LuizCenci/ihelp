"""
Testes para modelos de usuário.
"""
import pytest
from core.models import OngProfile, PersonProfile, Role
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestCustomUser:
    """Testes para o modelo CustomUser."""
    
    def test_create_volunteer(self):
        """Testa a criação de um voluntário."""
        user = User.objects.create_user(
            email='voluntario@test.com',
            password='testpass123',
            username='voluntario_test',
            role=Role.VOLUNTEER
        )
        assert user.email == 'voluntario@test.com'
        assert user.role == Role.VOLUNTEER
        assert user.check_password('testpass123')
        assert str(user) == f"voluntario_test ({user.get_role_display()})"
    
    def test_create_ong(self):
        """Testa a criação de uma ONG."""
        user = User.objects.create_user(
            email='ong@test.com',
            password='testpass123',
            username='ong_test',
            role=Role.ONG
        )
        assert user.email == 'ong@test.com'
        assert user.role == Role.ONG
        assert not user.is_staff
    
    def test_email_unique(self):
        """Testa que o email é único."""
        User.objects.create_user(
            email='unique@test.com',
            password='testpass123',
            username='user1'
        )
        with pytest.raises(Exception):  # IntegrityError
            User.objects.create_user(
                email='unique@test.com',
                password='testpass123',
                username='user2'
            )
    
    def test_superuser_creation(self):
        """Testa a criação de um superusuário."""
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        assert admin.is_superuser
        assert admin.is_staff
        assert admin.role == Role.ADMIN


@pytest.mark.django_db
class TestPersonProfile:
    """Testes para o modelo PersonProfile."""
    
    def test_create_person_profile(self):
        """Testa a criação de um perfil de pessoa."""
        user = User.objects.create_user(
            email='person@test.com',
            password='testpass123',
            username='person_test',
            role=Role.VOLUNTEER
        )
        profile = PersonProfile.objects.create(
            user=user,
            name='Pessoa Teste',
            cpf='12345678901',
            accept_announcements=True
        )
        assert profile.name == 'Pessoa Teste'
        assert profile.cpf == '12345678901'
        assert profile.accept_announcements is True


@pytest.mark.django_db
class TestOngProfile:
    """Testes para o modelo OngProfile."""
    
    def test_create_ong_profile(self):
        """Testa a criação de um perfil de ONG."""
        user = User.objects.create_user(
            email='ong@test.com',
            password='testpass123',
            username='ong_test',
            role=Role.ONG
        )
        profile = OngProfile.objects.create(
            user=user,
            ong_name='ONG Teste',
            cnpj='12345678901234',
            site='https://ong.test.com',
            is_approved=False
        )
        assert profile.ong_name == 'ONG Teste'
        assert profile.cnpj == '12345678901234'
        assert profile.is_approved is False
