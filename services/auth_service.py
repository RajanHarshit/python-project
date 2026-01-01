from repositories.user_repositories import UserRepository
from core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def signup(self, email: str, password: str):
        if self.user_repo.get_by_email(email):
            raise ValueError("User already exists")
        return self.user_repo.create(
            email=email,
            password_hash=hash_password(password),
        )
    
    def login(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return create_access_token(user.id)