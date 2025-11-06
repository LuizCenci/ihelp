
# Backend (Django) do projeto ihelp

Este diretório contém o backend do projeto ihelp, desenvolvido em Django. O objetivo é fornecer a base para autenticação, cadastro e gerenciamento de usuários e ONGs, servindo páginas web e, futuramente, APIs para integração com o frontend.

## Visão Geral

O backend atualmente implementa rotas e páginas para login e cadastro (Pessoa e ONG), com validação de campos e mensagens, mas sem persistência real de dados. O projeto está pronto para ser expandido com modelos, autenticação real e APIs REST.

## Estrutura do Projeto

- `manage.py` — utilitário do Django para comandos administrativos.
- `requirements.txt` — dependências do Python.
- `ihelp/` — configurações do projeto Django:
  - `settings.py` — configurações gerais (banco, apps, segurança).
  - `urls.py` — roteamento principal.
- `core/` — app principal:
  - `views.py` — views para home, login, cadastro de pessoa e ONG.
  - `urls.py` — rotas da aplicação.
  - `templates/core/` — templates HTML.
  - `static/core/` — arquivos estáticos (CSS).

## Instalação e Execução

1. Acesse o diretório `backend`:
  ```bash
  cd backend
  ```
2. Crie e ative um ambiente virtual:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
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
