from services.auth_service import auth_service

user = auth_service.login(
    "admin@skillswap.edu",
    "admin123"
)

print(user)