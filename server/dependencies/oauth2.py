"""
    Os tokens definirão scopes baseados nas FUNÇÕES dos usuários

    Os endpoints definirão scopes baseados em PERMISSÕES
    Cada FUNÇÃO pode ter várias PERMISSÕES vinculadas
"""

from fastapi.security import OAuth2PasswordBearer
from server.dependencies.get_environment_cached import get_environment_cached

environment = get_environment_cached()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{environment.AUTHENTICATOR_DNS}/users/token'
)

