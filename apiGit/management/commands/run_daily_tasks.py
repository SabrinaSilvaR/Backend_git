from django.core.management.base import BaseCommand

from apiGit import services


class Command(BaseCommand):
    help = 'Marks overdue loans, finishes old sanctions and expires temporary accounts'

    def handle(self, *args, **options):
        overdue = services.mark_overdue_loans()
        sanctions = services.finish_expired_sanctions()
        users = services.expire_temporary_accounts()
        self.stdout.write(f'Préstamos vencidos: {overdue}')
        self.stdout.write(f'Sanciones terminadas: {sanctions}')
        self.stdout.write(f'Cuentas temporales desactivadas: {users}')
