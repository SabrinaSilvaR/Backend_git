from rest_framework import serializers

# allowed email domains (see docs/analisis-preliminar.md, RF-01 and Student entity)
STAFF_DOMAINS = ['@inacap.cl']
STUDENT_DOMAINS = ['@inacap.cl', '@inacapmail.cl']

# RN-04: equipment can only be lent for 1, 3 or 6 hours
ALLOWED_HOURS = [1, 3, 6]


def validate_staff_email(email: str) -> str:
    email = email.lower()
    if not email.endswith(tuple(STAFF_DOMAINS)):
        raise serializers.ValidationError('El correo del personal debe ser @inacap.cl')
    return email


def validate_student_email(email: str) -> str:
    email = email.lower()
    if not email.endswith(tuple(STUDENT_DOMAINS)):
        raise serializers.ValidationError(
            'El correo del alumno debe ser @inacap.cl o @inacapmail.cl'
        )
    return email


def validate_rut(rut: str) -> str:
    """Checks a chilean RUT like 12345678-5 (without dots) using the modulo 11 rule."""
    rut = rut.replace('.', '').upper()
    if '-' not in rut:
        raise serializers.ValidationError('El RUT debe tener guion, ej: 12345678-5')

    number, dv = rut.split('-')
    if not number.isdigit() or len(dv) != 1:
        raise serializers.ValidationError('Formato de RUT inválido')

    # modulo 11 algorithm
    total = 0
    multiplier = 2
    for digit in reversed(number):
        total += int(digit) * multiplier
        multiplier += 1
        if multiplier > 7:
            multiplier = 2
    result = 11 - (total % 11)
    if result == 11:
        expected_dv = '0'
    elif result == 10:
        expected_dv = 'K'
    else:
        expected_dv = str(result)

    if dv != expected_dv:
        raise serializers.ValidationError('El dígito verificador del RUT no es válido')
    return rut


def validate_term(term_value: int, term_unit: str) -> None:
    """RN-04: hours must be 1, 3 or 6. Days can be any positive number."""
    if term_value <= 0:
        raise serializers.ValidationError({'term_value': 'El plazo debe ser mayor a 0'})
    if term_unit == 'HOURS' and term_value not in ALLOWED_HOURS:
        raise serializers.ValidationError(
            {'term_value': 'Para equipos el plazo solo puede ser 1, 3 o 6 horas'}
        )
