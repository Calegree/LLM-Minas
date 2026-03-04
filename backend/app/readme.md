## Backend

### Activar entorno virtual e iniciar servidor con reload
```bash
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Iniciar servidor

```bash
uvicorn app.main:app --port 8000
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```
## Actualizar dependencias

```bash
pip freeze > requirements.txt
```