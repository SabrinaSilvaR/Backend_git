## Proyecto Entorno Virtual Django

Repositorio con entorno virtual listo para ejecutar Django (Python) para clases de INACAP.

---

## Tabla de Contenidos
- [Proyecto Entorno Virtual Django](#proyecto-entorno-virtual-django)
- [Tabla de Contenidos](#tabla-de-contenidos)
- [🎓 Guía para Estudiantes e IA](#-guía-para-estudiantes-e-ia)
- [Prerrequisitos](#prerrequisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

---

## 🎓 Guía para Estudiantes e IA

Este repositorio cuenta con un sistema de agentes y habilidades de IA diseñado para el aprendizaje activo:
* 📖 [**`GUIA_ESTUDIANTES.md`**](GUIA_ESTUDIANTES.md): Manual paso a paso para aprender usando los agentes y habilidades.
* 💡 [**`exemplars.md`**](exemplars.md): Código de referencia modelo (Cheat Sheet) de modelos, serializers, vistas y servicios.
* 🤖 [**`AGENTS.md`**](AGENTS.md): Reglas de arquitectura y configuración de asistentes inteligentes.
* 📐 [**`docs/analisis-preliminar.md`**](docs/analisis-preliminar.md): Análisis preliminar del Sistema de Gestión de Biblioteca (problema, actores, entidades, modelo de datos, endpoints y consultas ORM).

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