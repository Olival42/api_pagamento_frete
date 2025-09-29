from modules.usuario.domain.entities import User
from modules.usuario.domain.repositories.user_repository import IUserRepository
from modules.usuario.domain.utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token
)

from modules.usuario.domain.repositories.blacklist_repository import IBlacklistRepository

class UserService:
    def __init__(self, user_repo: IUserRepository, blacklist_repo: IBlacklistRepository):
        self.user_repo = user_repo
        self.blacklist_repo = blacklist_repo

    def create_user(self, name: str, email: str, password: str) -> User:
        if self.user_repo.find_by_email(email):
            raise ValueError("Email já cadastrado")
        user = User(id=None, name=name, email=email, password=password)
        return self.user_repo.save(user)

    def login_user(self, email: str, password: str) -> dict:
        user = self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Email ou senha inválidos")

        if not User.verify_password(password, user.password):
            raise ValueError("Email ou senha inválidos")

        access_token = create_access_token(user.id, user.email)

        refresh_token = create_refresh_token(user.id, user.email)

        return {
                "user": user, 
                "access": access_token, 
                "refresh": refresh_token
            }
    
    def logout(self, token: str) -> dict:
        try:
            payload = decode_token(token)
            jti = payload["jti"]    
            exp = payload["exp"]
            self.blacklist_repo.add_token(jti, exp)
            return {"detail": "Logout realizado com sucesso"}
        except ValueError as e:
            return {"detail": str(e)}
        
    def authenticate(self, token: str) -> dict:
        payload = decode_token(token)
        if self.blacklist_repo.is_blacklisted(payload["jti"]):
            raise ValueError("Token revogado")
        return payload
