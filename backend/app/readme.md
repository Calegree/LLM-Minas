## Backend

### Activar entorno virtual
```bash
cd backend
.\.venv\Scripts\activate
```

### Iniciar servidor

```bash
uvicorn app.main:app --port 8000
```

### Iniciar servidor con reload

```bash
uvicorn app.main:app --reload --port 8000
```
## Instalar dependencias

```bash
pip install -r requirements.txt
```
## Actualizar dependencias

```bash
pip freeze > requirements.txt
```