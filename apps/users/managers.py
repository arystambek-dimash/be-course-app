from django.contrib.auth.base_user import BaseUserManager
from apps.utils.managers import NotDeletedManager


class UserManager(NotDeletedManager, BaseUserManager):
    use_in_migrations = True

    def create_user(self, username: str, password: str = None):
        if not username:
            raise ValueError('Must have username')
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password) -> None:
        user = self.create_user(
            username,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
