from django.db import transaction

@transaction.atomic
def execute____service_name___(*, name: str) -> dict[str, str]:
    """
    Business service to execute ___service_name___.
    """
    clean_name = name.strip()
    return {"status": "success", "name": clean_name}
