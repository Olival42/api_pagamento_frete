from modules.usuario.domain.entities import User
from modules.usuario.domain.repositories.user_repository import IUserRepository
from modules.usuario.domain.utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token
)

from modules.usuario.domain.repositories.blacklist_repository import IBlacklistRepository

import os 
import redis 
from dotenv import load_dotenv 

load_dotenv() 

REDIS_HOST = os.getenv("REDIS_HOST") 
REDIS_PORT = os.getenv("REDIS_PORT") 
REDIS_DB = os.getenv("REDIS_DB") 

r = redis.Redis(host=str(REDIS_HOST), port=int(REDIS_PORT), db=int(REDIS_DB)) 

MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS")) 
LOCK_TIME_SECONDS = int(os.getenv("LOCK_TIME_SECONDS"))

class UserService:
    def __init__(self, user_repo: IUserRepository, blacklist_repo: IBlacklistRepository):
        self.user_repo = user_repo
        self.blacklist_repo = blacklist_repo

    def create_user(self, name: str, email: str, password: str) -> User:
        if self.user_repo.find_by_email(email):
            raise ValueError("Email já cadastrado")
        
        user = User(id=None, name=name, email=email, password=password)
        
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)
        
        saved_user = self.user_repo.save(user)
        
        expires_at = decode_token(access_token)["exp"]
        
        return {
            "id": saved_user.id,
            "name": saved_user.name,
            "email": saved_user.email,
            "access": access_token,
            "refresh": refresh_token,
            "expires_at": expires_at
        }

    def login_user(self, email: str, password: str) -> dict: 
        user = self.user_repo.find_by_email(email) 
        
        attempts_key = f"login_attempts:{email}" 
        
        attempts = r.get(attempts_key) 
        
        if attempts and int(attempts) >= MAX_LOGIN_ATTEMPTS: 
            raise ValueError("Conta temporariamente bloqueada. Tente novamente mais tarde.") 
        
        if not user or not User.verify_password(password, user.password): 
            r.incr(attempts_key) 
            r.expire(attempts_key, LOCK_TIME_SECONDS) 
            raise ValueError("Email ou senha inválidos") 
        
        r.delete(attempts_key) 
        
        access_token = create_access_token(user.id, user.email) 
        refresh_token = create_refresh_token(user.id, user.email) 
        
        payload = decode_token(access_token)
        expires_at = payload["exp"]
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "access": access_token,
            "refresh": refresh_token,
            "expires_at": expires_at
        }
    
    def logout(self, access_token: str, refresh_token: str = None) -> dict:
        try:
            payload = decode_token(access_token)
            
            jti = payload["jti"]
            exp = payload["exp"]
            
            if not self.blacklist_repo.is_blacklisted(jti):
                self.blacklist_repo.add_token(jti, exp)
            
            if refresh_token:
                payload_r = decode_token(refresh_token)
                
                jti_r = payload_r["jti"]
                exp_r = payload_r["exp"]
                
                if not self.blacklist_repo.is_blacklisted(jti_r):
                    self.blacklist_repo.add_token(jti_r, exp_r)
            
            return {"detail": "Logout realizado com sucesso"}
        except ValueError as e:
            return {"detail": str(e)}

        
    def refresh_access_token(self, refresh_token: str) -> dict: 
        try: 
            payload = decode_token(refresh_token)
            
            jti = payload["jti"] 
            
            if self.blacklist_repo.is_blacklisted(jti): 
                raise ValueError("Refresh token revogado") 
            
            new_access_token = create_access_token(payload["user_id"], payload["email"]) 
            
            return {"access": new_access_token} 
        except ValueError as e: 
            raise ValueError(str(e))
        
    def authenticate(self, token: str) -> dict:
        payload = decode_token(token)
        
        if self.blacklist_repo.is_blacklisted(payload["jti"]):
            raise ValueError("Token revogado")
        
        return payload
