from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cria contas padrão de voluntário e ONG para testes rápidos.'

    def handle(self, *args, **options):
        User = get_user_model()
        # Voluntário
        if not User.objects.filter(email='voluntario@ihelp.com').exists():
            User.objects.create_user(
                email='voluntario@ihelp.com',
                password='123456',
                username='voluntario',
                role='VOLUNTARIO',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Usuário voluntário criado: voluntario@ihelp.com / 123456'))
        else:
            self.stdout.write('Usuário voluntário já existe.')
        # ONG
        if not User.objects.filter(email='ong@ihelp.com').exists():
            User.objects.create_user(
                email='ong@ihelp.com',
                password='123456',
                username='ong',
                role='ONG',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Usuário ONG criado: ong@ihelp.com / 123456'))
        else:
            self.stdout.write('Usuário ONG já existe.')
