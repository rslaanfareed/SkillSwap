from password_utils import PasswordManager

password = "admin123"

hashed = PasswordManager.hash_password(password)

print("Hash:")
print(hashed)

print()

print(
    PasswordManager.verify_password(
        "admin123",
        hashed
    )
)

print(
    PasswordManager.verify_password(
        "wrongpassword",
        hashed
    )
)