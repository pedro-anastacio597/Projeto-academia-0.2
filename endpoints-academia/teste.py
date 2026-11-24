from passlib.context import CryptContext

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

senha = "Teste123"

hash_senha = bcrypt_context.hash(senha)

print(bcrypt_context.verify(senha, hash_senha))