## Contas padrão para login rápido

Após rodar as migrations, crie contas de teste executando:

```bash
python manage.py create_default_users
```

Contas criadas:

- Voluntário:  
  email: voluntario@ihelp.com  
  senha: 123456
- ONG:  
  email: ong@ihelp.com  
  senha: 123456

Use esses dados para login rápido no sistema.

# Backend (Django) do projeto ihelp

Este diretório contém o backend do projeto ihelp, desenvolvido em Django. O objetivo é fornecer a base para autenticação, cadastro e gerenciamento de usuários, ONGs e vagas de voluntariado, servindo páginas web e, futuramente, APIs REST para integração com o frontend.

## 🎯 Visão Geral

O backend implementa um sistema completo de cadastro e gerenciamento com:
- **Autenticação customizada** com email como username
- **Dois tipos de usuários**: Voluntários e ONGs com perfis específicos
- **Sistema de vagas e anúncios** para oportunidades de voluntariado
- **Validações robustas** de CPF/CNPJ
- **Admin Django integrado** para gerenciamento
- **PostgreSQL** como banco de dados principal
- **Testes automatizados** com pytest

## 📁 Estrutura do Projeto

```
backend/
├── manage.py                      # Utilitário Django
├── .tool-versions                 # Configuração para mise/asdf
├── .env.example                   # Exemplo de variáveis de ambiente
├── docker-compose.yml             # Serviço PostgreSQL
├── requirements.txt               # Dependências Python
├── pytest.ini                     # Configuração de testes
├── conftest.py                    # Setup do pytest
├── ihelp/                         # Projeto Django
│   ├── settings.py               # Configurações
│   ├── urls.py                   # URLs principais
│   ├── wsgi.py                   # WSGI para produção
│   └── asgi.py                   # ASGI para produção
└── core/                          # App principal
    ├── models.py                 # Modelos (CustomUser, Posts, etc)
    ├── views.py                  # Views/lógica
    ├── forms.py                  # Formulários
    ├── urls.py                   # URLs da app
    ├── admin.py                  # Admin Django
    ├── validators.py             # Validadores customizados
    ├── tests.py                  # Testes
    ├── templates/                # Templates HTML
    ├── static/                   # CSS, JS, imagens
    └── management/commands/      # Comandos customizados
        └── create_default_users.py
```

## 🚀 Instalação e Execução com mise/asdf

### Pré-requisitos
- Docker e Docker Compose
- mise ou asdf instalado

### Passos de Instalação

1. **Acesse o diretório backend:**
   ```bash
   cd backend
   ```

2. **O arquivo `.tool-versions` já define Python 3.11:**
   ```bash
   mise install
   # ou se usar asdf
   asdf install
   ```

3. **Garanta que o ambiente Python está ativado:**
   ```bash
   mise activate
   ```

4. **Se necessário, instale pip manualmente:**
   ```bash
   python -m ensurepip --upgrade
   ```

5. **Crie arquivo `.env` a partir do exemplo:**
   ```bash
   cp .env.example .env
   ```
   Edite os valores conforme necessário (para desenvolvimento, os padrões funcionam).

6. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. **Suba o banco de dados PostgreSQL:**
   ```bash
   docker-compose up -d
   ```

8. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

9. **Crie contas de teste:**
   ```bash
   python manage.py create_default_users
   ```

10. **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

11. **Acesse em:** http://127.0.0.1:8000/

## 🔐 Contas padrão para login

## 🔐 Contas padrão para login

Após criar as contas padrão, você pode logar com:

- **Voluntário:**
  - Email: `voluntario@ihelp.com`
  - Senha: `123456`

- **ONG:**
  - Email: `ong@ihelp.com`
  - Senha: `123456`

- **Admin (Django):**
  ```bash
  python manage.py createsuperuser
  ```
  Acesse em: http://127.0.0.1:8000/admin/

## 📊 Rotas Principais

- `/` — Página inicial (home)
- `/login/` — Login de usuários
- `/logout/` — Logout
- `/cadastro/` — Escolha entre voluntário e ONG
- `/cadastro/pessoa/` — Cadastro de voluntário
- `/cadastro/ong/` — Cadastro de ONG
- `/criar-anuncio/` — Criar vagas (apenas ONGs)
- `/vagas/<id>` — Visualizar detalhes de uma vaga
- `/admin/` — Painel administrativo

## 🧪 Testes Automatizados

Execute os testes com pytest:

```bash
# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=core

# Gerar relatório HTML de cobertura
pytest --cov=core --cov-report=html
# Relatório estará em: htmlcov/index.html

# Rodar teste específico
pytest core/tests.py::TestCustomUser::test_create_volunteer -v
```

## 🔒 Segurança e Configuração para Produção

### Variáveis de Ambiente Críticas

Criar um arquivo `.env` com:

```
SECRET_KEY=sua-chave-secreta-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DB_HOST=seu-servidor-postgres.com
DB_NAME=ihelp_prod
DB_USER=usuario_db
DB_PASSWORD=senha-segura-aqui
```

### Checklist de Segurança

- [ ] Nunca exponha `SECRET_KEY` no repositório
- [ ] Mantenha `DEBUG=False` em produção
- [ ] Configure `ALLOWED_HOSTS` com domínios reais
- [ ] Use HTTPS/SSL em produção
- [ ] Rotine backups do banco PostgreSQL
- [ ] Configure email para notificações
- [ ] Implemente rate limiting e proteção contra brute force
- [ ] Use variáveis de ambiente via `.env` seguro

## 🐳 Docker e Deploy

### Usar Docker para PostgreSQL (Desenvolvimento)

```bash
docker-compose up -d      # Inicia
docker-compose logs -f db # Ver logs
docker-compose down       # Para
```

### Deploy em Produção

Recomendações:
1. Use **Gunicorn** como servidor WSGI
2. Configure **Nginx** como proxy reverso
3. Use **SSL/TLS** com Let's Encrypt
4. Configure **Postgres** em servidor dedicado
5. Use **Supervisord** ou systemd para manter o serviço rodando

Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn ihelp.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## 📦 Dependências Principais

```
Django==5.2.7             # Framework web
psycopg2-binary==2.9.10   # Cliente PostgreSQL
django-widget-tweaks==1.5.0  # Widgets para templates
django-environ==0.11.2    # Variáveis de ambiente
pytest==8.0.0             # Framework de testes
pytest-django==4.7.0      # Plugin pytest para Django
pytest-cov==5.0.0         # Cobertura de testes
```

## 🔍 Modelos de Dados

### CustomUser
Usuario customizado com email como USERNAME_FIELD.
Roles: ADMIN, ONG, VOLUNTEER

### PersonProfile
Perfil de voluntário (CPF, nome, aceitação de avisos)

### OngProfile
Perfil de ONG (CNPJ, site, endereço, descrição, aprovação)

### PostAnnouncement
Vagas/anúncios criados por ONGs

### PostFeed
Posts/atualizações da ONG

### Category
Categorias para vagas

### Comment
Comentários em PostFeed

### Application
Inscrições de voluntários em vagas

## 🛠️ Comandos Úteis

```bash
# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Criar usuários padrão
python manage.py create_default_users

# Shell Django interativo
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Limpar cache
python manage.py clear_cache

# Resetar banco (cuidado!)
python manage.py flush
```

## 📝 Como Contribuir

1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feat/minha-feature
   ```

2. Faça commits claros e objetivos:
   ```bash
   git commit -m "feat: adiciona validação de CPF"
   ```

3. Escreva testes para suas mudanças

4. Execute testes antes de enviar:
   ```bash
   pytest
   ```

5. Envie um Pull Request detalhando suas alterações

## 🚦 Próximos Passos

- [ ] Implementar autenticação com tokens (JWT)
- [ ] Criar API REST com Django REST Framework
- [ ] Adicionar sistema de avaliações
- [ ] Implementar busca e filtros avançados
- [ ] Configurar email de notificações
- [ ] Adicionar CI/CD com GitHub Actions
- [ ] Melhorar performance com caching
- [ ] Implementar log estruturado

## 📚 Referências

- [Documentação Django 5.2](https://docs.djangoproject.com/pt-br/5.2/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pytest-Django](https://pytest-django.readthedocs.io/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## 📞 Suporte

Em caso de dúvidas ou sugestões:
- Abra uma **issue** no repositório
- Entre em contato com os mantenedores
- Consulte a documentação oficial do Django


## Usando mise para gerenciar o ambiente

Se você utiliza o [mise](https://mise.jdx.dev/) (gerenciador de ambientes para múltiplas linguagens), pode garantir a versão correta do Python e isolar dependências facilmente:

1. Instale o mise seguindo as instruções do site oficial.
2. No diretório `backend`, defina a versão do Python desejada (exemplo: 3.11):
  ```bash
  mise use python@3.11
  mise install
  ```
  Isso instalará o Python e criará um ambiente isolado para o projeto.
3. Ative o ambiente (se necessário):
  ```bash
  mise activate
  ```

4. Caso o comando `pip` não esteja disponível após instalar o Python pelo mise, instale o pip manualmente:
   ```bash
   python -m ensurepip --upgrade
   ```
   Depois, instale as dependências normalmente:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Siga os passos de migração e execução abaixo.

---


## Instalação e Execução

1. Acesse o diretório `backend`:
   ```bash
   cd backend
   ```
2. Garanta que o ambiente Python está ativado pelo mise/asdf (veja instruções acima).
3. Instale as dependências:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Execute as migrações iniciais:
   ```bash
   python manage.py migrate
   ```
5. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
6. Acesse em: http://127.0.0.1:8000/

### Observações
- O banco padrão é SQLite (`db.sqlite3`).
- Para usar PostgreSQL, ajuste `DATABASES` em `ihelp/settings.py` e configure as variáveis de ambiente.
- O arquivo `requirements.txt` já inclui `psycopg2` para PostgreSQL.

## Rotas Disponíveis

- `/` — Página inicial (home)
- `/login/` — Login (simulado, sem autenticação real)
- `/cadastro/pessoa/` — Cadastro de Pessoa (validação de campos)
- `/cadastro/ong/` — Cadastro de ONG (validação de campos e termos)

## Segurança e Produção

- **SECRET_KEY**: Nunca exponha a chave secreta em produção. Use variáveis de ambiente.
- **DEBUG**: Mantenha `DEBUG = False` em produção.
- **ALLOWED_HOSTS**: Defina os domínios permitidos antes de publicar.
- **Banco de Dados**: Use PostgreSQL ou outro banco robusto em produção.
- Recomenda-se criar um arquivo `.env` e usar pacotes como `python-decouple` ou `django-environ` para variáveis sensíveis.

## Como Contribuir

1. Crie um fork do projeto.
2. Crie uma branch para sua feature/correção:
  ```bash
  git checkout -b minha-feature
  ```
3. Faça commits claros e objetivos.
4. Envie um Pull Request detalhando suas alterações.

## Próximos Passos Sugeridos

- Implementar modelos para persistência de usuários e ONGs.
- Adicionar autenticação real (Django Auth ou customizada).
- Criar testes automatizados para views e formulários.
- Expor APIs RESTful (Django REST Framework).
- Melhorar documentação e exemplos de deploy.

## Referências

- [Documentação Django](https://docs.djangoproject.com/pt-br/5.2/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---
Em caso de dúvidas ou sugestões, abra uma issue ou entre em contato com os mantenedores.
