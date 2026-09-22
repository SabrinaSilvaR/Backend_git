# Resumen del Código Implementado — Sistema de Biblioteca (`apiGit`)

> Documento de apoyo para estudiantes: explica **qué hace cada archivo**, **qué cumple cada
> función/clase** y **aclara los términos de Django/DRF de mayor complejidad** usados en la
> implementación actual (commit `1cee396`). No reemplaza al README ni a
> [`docs/analisis-preliminar.md`](analisis-preliminar.md) (que cubre el análisis del problema);
> este documento describe el **código ya escrito**.

---

## Tabla de Contenidos

- [Visión general](#visión-general)
- [`models.py` — Modelos de dominio](#modelspy--modelos-de-dominio)
- [`serializers.py` — Serializadores DRF](#serializerspy--serializadores-drf)
- [`views.py` — Vistas / ViewSets](#viewspy--vistas--viewsets)
- [`urls.py` — Enrutamiento](#urlspy--enrutamiento)
- [`admin.py` — Panel de administración](#adminpy--panel-de-administración)
- [Configuración relevante (`settings.py`)](#configuración-relevante-settingspy)
- [Glosario de términos complejos](#glosario-de-términos-complejos)
- [Pendientes / puntos a revisar](#pendientes--puntos-a-revisar)

---

## Visión general

La app `apiGit` implementa el backend de un sistema de préstamos de biblioteca (libros,
tablets, audífonos, etc.) para estudiantes de INACAP. Actualmente expone **8 modelos**, sus
**serializadores**, **vistas tipo ViewSet** y las **rutas REST** correspondientes, todo
registrado además en el panel de administración de Django.

La arquitectura objetivo del proyecto (ver `AGENTS.md`) separa la lógica en:

| Capa | Archivo | Estado actual |
| --- | --- | --- |
| Esquema de datos | `models.py` | ✅ Implementado |
| Validación/transformación | `serializers.py` | ✅ Implementado (básico) |
| Lógica de negocio (escritura) | `services.py` | ⛔ No existe todavía |
| Consultas de lectura complejas | `selectors.py` | ⛔ No existe todavía |
| HTTP / request-response | `views.py` | ✅ Implementado (básico) |
| Validaciones reutilizables | `validations.py` | ⚠️ Archivo vacío |

---

## `models.py` — Modelos de dominio

### `User(AbstractUser)`
Representa al **personal de la biblioteca** (administradores y operadores de mesón), **no** a
los estudiantes.

- `role`: distingue `ADMIN` de `OPERATOR` usando un `TextChoices` (enum de Django).
- `is_temporary`, `valid_from`, `valid_until`: soportan cuentas de acceso temporal (RF-03) con
  expiración automática.
- `mfa_secret`: campo para guardar el secreto de un segundo factor de autenticación (TOTP).
- Se configura como modelo de usuario del proyecto vía `AUTH_USER_MODEL = 'apiGit.User'`
  en `settings.py` (ver más abajo).

### `Student`
Estudiante que puede tomar préstamos. **No inicia sesión en el sistema** (no hereda de
`AbstractUser`); solo se guarda su identidad (`rut`, correo institucional, nombre) y si está
`is_active` (borrado lógico / *soft delete*).

### `Category`
Tipo de recurso prestable (Libro, Tablet, Audífono...). Define la **unidad del plazo de
préstamo** (`term_unit`: horas o días), que luego heredan tanto `ResourceTitle`/`ResourceItem`
como cada `Loan`.

### `ResourceTitle` y `ResourceItem`
Modelan la diferencia entre **título** y **ejemplar físico**, igual que un catálogo de
biblioteca real:

- `ResourceTitle`: el "libro" en abstracto (título, autor/marca, código de referencia/ISBN).
- `ResourceItem`: **un ejemplar concreto** de ese título (código de barras único, ubicación,
  estado: `AVAILABLE`, `ON_LOAN`, `MAINTENANCE`, `RETIRED`). Un mismo título puede tener varios
  ejemplares (`ForeignKey` con `related_name="items"`).

### `Loan`
El préstamo en sí. Relaciona un `ResourceItem` con un `Student`, y registra qué operador lo
entregó (`checked_out_by`) y cuál lo recibió de vuelta (`checked_in_by`).

- `due_at` se calcula a partir de `term_value` + `term_unit` (ese cálculo debería vivir en
  `services.py`, todavía no implementado).
- Tiene una **restricción a nivel de base de datos** (`UniqueConstraint` con `condition`) que
  impide que el mismo `ResourceItem` tenga dos préstamos `ACTIVE` simultáneos — ver el glosario
  para el detalle técnico.

### `LoanReceipt`
Comprobante de entrega enviado por correo (`OneToOneField` con `Loan`: **un** préstamo tiene
**como máximo un** comprobante).

### `Sanction`
Bloqueo aplicado a un estudiante por atraso en la devolución (`minutes_late`, período de
bloqueo `starts_at`/`ends_at`, regla aplicada).

### `AuditLog`
Bitácora de auditoría genérica: quién (`user`), qué acción (`action`, ej. `LOAN_CREATED`), sobre
qué entidad (`entity_name` + `entity_id`) y desde qué IP.

---

## `serializers.py` — Serializadores DRF

Un `ModelSerializer` por cada modelo (`UserSerializer`, `StudentSerializer`,
`CategorySerializer`, `ResourceTitleSerializer`, `ResourceItemSerializer`, `LoanSerializer`,
`SanctionSerializer`, `AuditLogSerializer`). Todos siguen el mismo patrón mínimo:

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
```

Su función es **traducir** entre instancias de modelo (Python/ORM) y JSON (entrada/salida de la
API), además de validar los datos recibidos antes de guardarlos.

En `UserSerializer` hay un `create()` **comentado** que muestra cómo debería crearse un usuario
usando `User.objects.create_user(...)` (para que Django **hashee la contraseña**, en vez de
guardarla en texto plano si se usara `create()` por defecto del `ModelSerializer`).

---

## `views.py` — Vistas / ViewSets

Cada modelo tiene un `ModelViewSet` (`UserViewSet`, `StudentViewSet`, etc.):

```python
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
```

Un `ModelViewSet` de DRF **genera automáticamente** las 5 operaciones REST estándar (list,
create, retrieve, update/partial_update, destroy) sin escribir cada método a mano — ver glosario.

---

## `urls.py` — Enrutamiento

Usa un `DefaultRouter` de DRF, que registra cada `ViewSet` bajo un prefijo y genera las URLs
(`/users/`, `/students/`, `/categories/`, `/resource-titles/`, `/resource-items/`, `/loans/`,
`/sanctions/`, `/audit-logs/`) junto con las variantes de detalle (`/loans/<id>/`, etc.) y,
gracias al `DefaultRouter`, también una vista raíz navegable de la API.

---

## `admin.py` — Panel de administración

Registra todos los modelos en el admin de Django con una sola línea:

```python
admin.site.register([Sanction, Student, ResourceItem, ResourceTitle, Loan, LoanReceipt, Category, AuditLog, User])
```

Esto habilita un CRUD visual en `/admin/` para cada modelo, útil para inspeccionar datos durante
el desarrollo sin necesidad de usar la API o el shell.

---

## Configuración relevante (`settings.py`)

- `AUTH_USER_MODEL = 'apiGit.User'`: le indica a Django que use el modelo `User` **personalizado**
  de `apiGit` en vez del `User` por defecto de `django.contrib.auth`. Esto es lo que permite
  agregar campos como `role` o `is_temporary` directamente al usuario del sistema.
- `INSTALLED_APPS` incluye `apiGit` y `rest_framework`.

---

## Glosario de términos complejos

> Cada término tiene una línea **"En simple"** (la idea en lenguaje cotidiano) y luego el
> detalle técnico con su uso concreto en este proyecto.

- **`AbstractUser`**
  *En simple:* es un "molde" que trae Django ya hecho, con todo lo necesario para que alguien
  pueda iniciar sesión (usuario, contraseña encriptada, permisos...). Tú no escribes esa parte de
  cero: heredas de él y solo agregas los campos que te faltan.
  *Detalle técnico:* clase base de Django para crear un modelo de usuario propio conservando todo
  el sistema de autenticación (`is_staff`, `is_superuser`, permisos, grupos, hash de contraseña,
  etc.). En este proyecto, `class User(AbstractUser)` agrega `role`, `is_temporary`,
  `valid_from`/`valid_until` y `mfa_secret` encima de esa base.

- **`TOTP`** *(Time-based One-Time Password)*
  *En simple:* es el código de 6 dígitos que cambia cada 30 segundos en apps como Google
  Authenticator. Es un segundo factor de autenticación (2FA): además de la contraseña, la persona
  debe ingresar ese código para demostrar que tiene el dispositivo/app registrado.
  *Detalle técnico:* el código se genera combinando una **clave secreta compartida** (guardada en
  `mfa_secret`) con la hora actual, usando un algoritmo estándar (RFC 6238). El campo `mfa_secret`
  en `User` es donde se guardaría esa clave para poder validar los códigos que ingresa el
  operador/administrador al iniciar sesión.

- **`TextChoices` (enum)**
  *En simple:* un *enum* es "una lista cerrada de opciones válidas, cada una con un nombre".
  En vez de escribir el texto `"ADMIN"` a mano en distintas partes del código (con riesgo de
  typo, ej. `"ADMNI"`), defines `Role.ADMIN` una sola vez y lo reutilizas con autocompletado.
  *Detalle técnico:* forma moderna de Django para declarar las opciones de un `CharField`. Da
  autocompletado (`Loan.Status.ACTIVE`) y valida automáticamente que el valor guardado sea uno de
  los permitidos — no se puede guardar un string arbitrario por error.

- **`on_delete=models.PROTECT`**
  *En simple:* si intentas borrar un registro "padre" (ej. un `Student`) que todavía tiene
  registros "hijos" dependiendo de él (sus `Loan`), Django **no te deja borrarlo** y lanza un
  error.
  *Detalle técnico:* evita perder historial de préstamos por accidente. Es más estricto que
  `CASCADE` (que borraría en cascada todo lo relacionado) o `SET_NULL` (que dejaría el campo
  vacío).

- **`related_name`**
  *En simple:* el "nombre para volver" desde el otro lado de una relación. Si `ResourceItem`
  apunta a `ResourceTitle`, `related_name` es cómo, desde un `ResourceTitle`, accedes a todos sus
  `ResourceItem`.
  *Detalle técnico:* ej. `ResourceTitle.items` (gracias a `related_name="items"`) en vez del
  nombre por defecto que generaría Django, `resourceitem_set`.

- **`UniqueConstraint(fields=..., condition=...)`** *(restricción única condicional)*
  *En simple:* una regla de "no se puede repetir" que **solo aplica en ciertos casos**, no
  siempre.
  *Detalle técnico:* a diferencia de `unique=True` (que aplica siempre), esta combinación solo
  impide duplicados **cuando se cumple la condición** (`status="ACTIVE"`). En `Loan` esto permite
  que un mismo `ResourceItem` tenga **muchos préstamos históricos** (`RETURNED`), pero **nunca
  dos activos a la vez** — la regla de negocio vive en la base de datos, no solo en el código
  Python.

- **`OneToOneField`**
  *En simple:* como una `ForeignKey`, pero limitada a **una sola relación por registro** (uno a
  uno, no uno a muchos).
  *Detalle técnico:* ej. un `Loan` tiene como máximo un `LoanReceipt` y como máximo una
  `Sanction` asociados.

- **`auto_now_add=True`**
  *En simple:* Django rellena la fecha/hora automáticamente **solo la primera vez** que se crea
  el registro, y después ya no se puede cambiar.
  *Detalle técnico:* distinto de `auto_now=True`, que se actualiza en **cada** `save()` (útil para
  un campo tipo "última modificación").

- **`ModelViewSet`**
  *En simple:* una clase de DRF que te da "gratis" las operaciones típicas de un CRUD (crear,
  leer, actualizar, borrar) sin que tengas que escribir cada vista HTTP a mano.
  *Detalle técnico:* combina lectura y escritura completas (`list`, `create`, `retrieve`,
  `update`, `partial_update`, `destroy`) a partir de un `queryset` y un `serializer_class`.

- **`DefaultRouter`**
  *En simple:* genera automáticamente las URLs de la API a partir de tus `ViewSet`, siguiendo
  siempre el mismo patrón (`/recurso/` y `/recurso/<id>/`).
  *Detalle técnico:* utilidad de DRF que registra cada `ViewSet` y produce tanto las rutas de
  lista/detalle como una vista raíz navegable de la API (útil para explorar los endpoints desde
  el navegador).

- **`ModelSerializer` con `fields = '__all__'`**
  *En simple:* le dices al serializador "incluye todos los campos del modelo, tal cual", sin
  elegir uno por uno.
  *Detalle técnico:* es rápido para prototipar, pero **`AGENTS.md` pide usar `fields` explícitos**
  (ver sección "Pendientes" abajo) porque `'__all__'` puede exponer sin querer campos sensibles
  (ej. `password`, `mfa_secret`) en la respuesta de la API.

---

## Pendientes / puntos a revisar

Estas observaciones son para que, como estudiante, las trabajes tú mismo (no son errores
bloqueantes, sino oportunidades de práctica alineadas con `AGENTS.md`):

1. **`validations.py` está vacío.** Es el lugar sugerido para validadores reutilizables (ej.
   validar que el correo termine en `@inacap` o `@inacapmail`, mencionado en el comentario de
   `Student.institutional_email`).
2. **Falta `services.py` y `selectors.py`.** Reglas de negocio como "calcular `due_at` según
   `term_value`/`term_unit`", "marcar un préstamo `OVERDUE`" o "aplicar una `Sanction`
   automáticamente" no deberían vivir en las vistas ni en los serializadores.
3. **`fields = '__all__'` en todos los serializadores.** `AGENTS.md` pide especificar los campos
   explícitamente; esto es especialmente importante en `UserSerializer`, que hoy expondría
   `password` y `mfa_secret` tal cual en la API.
4. **`UserSerializer.create()` está comentado.** Sin él, crear un `User` vía API guarda la
   contraseña en texto plano en vez de hashearla con `create_user()`.
5. **Las vistas no restringen permisos** (`permission_classes`). Endpoints como `/users/` o
   `/audit-logs/` deberían protegerse al menos con `IsAuthenticated` / `IsAdminUser`.
