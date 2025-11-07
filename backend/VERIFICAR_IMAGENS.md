# Verificação de Upload de Imagens

## Problemas Identificados e Correções

### 1. Formulário
- ✅ Alterado widget de `FileInput` para `ClearableFileInput` (melhor para ImageField)
- ✅ Método `save()` simplificado para garantir que o arquivo seja salvo corretamente

### 2. Configurações
- ✅ `MEDIA_URL` e `MEDIA_ROOT` configurados em `settings.py`
- ✅ URLs de mídia configuradas em `urls.py` (apenas em DEBUG)

### 3. Templates
- ✅ Adicionado fallback visual quando imagem não existe
- ✅ Tratamento de erro na exibição de imagens

## Verificações Necessárias

### 1. Verificar se DEBUG está ativado
```python
# Em settings.py, verifique:
DEBUG = env('DEBUG', default=False)  # Deve ser True em desenvolvimento
```

### 2. Verificar se a migration foi aplicada
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Verificar se o diretório existe
```bash
mkdir -p media/announcements
chmod 755 media/announcements
```

### 4. Verificar dados no banco
Execute no shell do Django:
```python
from core.models import PostAnnouncement
for anuncio in PostAnnouncement.objects.all():
    print(f"ID: {anuncio.id}, Title: {anuncio.title}")
    print(f"Photo field type: {type(anuncio.photo)}")
    print(f"Photo value: {anuncio.photo}")
    if anuncio.photo:
        print(f"Photo URL: {anuncio.photo.url}")
        print(f"Photo path: {anuncio.photo.path}")
    print("---")
```

### 5. Verificar se arquivos estão sendo salvos
```bash
ls -la media/announcements/
```

### 6. Testar upload manualmente
1. Acesse o formulário de criação de anúncio
2. Selecione uma imagem
3. Verifique se o preview aparece
4. Salve o formulário
5. Verifique se o arquivo foi criado em `media/announcements/`
6. Verifique se a imagem aparece na listagem

## Possíveis Problemas

### Problema 1: DEBUG = False
**Solução**: Configure `DEBUG=True` no `.env` ou em `settings.py`

### Problema 2: Migration não aplicada
**Solução**: Execute `python manage.py makemigrations` e `python manage.py migrate`

### Problema 3: Dados antigos (CharField)
**Solução**: Se houver dados antigos com URLs em texto, você precisará:
1. Criar uma migration de dados para converter ou limpar
2. Ou deletar os anúncios antigos e recriar

### Problema 4: Permissões de diretório
**Solução**: 
```bash
chmod 755 media/
chmod 755 media/announcements/
```

### Problema 5: Servidor não está servindo arquivos estáticos
**Solução**: Certifique-se de que está rodando com `DEBUG=True` e que o `urls.py` tem a configuração de mídia


