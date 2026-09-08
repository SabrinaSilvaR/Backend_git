## Proyecto Entorno Virtual Django

Repositorio con entorno virtual listo para ejecutar Django (Python) para clases de INACAP.

---

## Tabla de Contenidos
- [Proyecto Entorno Virtual Django](#proyecto-entorno-virtual-django)
- [Tabla de Contenidos](#tabla-de-contenidos)
- [Prerrequisitos](#prerrequisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

---

## Prerrequisitos
- Disponer de un IDE (por ejemplo, VS Code o PyCharm).
- Python 3.x instalado.
- Entorno virtual activado.

---

## Instalación y Configuración

Comandos para inicializar y configurar el proyecto:

```bash
# Generar scripts de migración basados en los modelos definidos
python manage.py makemigrations

# Aplicar las migraciones a la base de datos
python manage.py migrate

# Crear superusuario para acceder al panel de administración de Django
python manage.py createsuperuser

# Ejecutar el servidor de desarrollo local
python manage.py runserver
```

---

## Uso
Utilizar como repositorio base para el desarrollo de APIs REST y creación de nuevos modelos durante las clases.

---

## Tecnologías Utilizadas
- **Lenguaje de Programación:** Python
- **Framework Web:** Django
- **API Toolkit:** Django REST Framework