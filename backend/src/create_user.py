import asyncio
from getpass import getpass
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from db.engine import sessionmanager
from db.models import User
from api.schemas.user import UserCreate
from hashing import Hasher


async def create_user():
    try:
        name = input("Имя пользователя: ").strip()
        email = input("Email: ").strip()
        password = getpass("Пароль: ").strip()

        user_data = UserCreate(name=name, email=email, password=password)

    except ValidationError as ve:
        print("\nОшибка валидации:")
        for error in ve.errors():
            loc = " → ".join(str(i) for i in error["loc"])
            print(f"  [{loc}] {error['msg']}")
        return

    try:
        async with sessionmanager.session() as session:
            user = User(
                name=user_data.name,
                email=user_data.email,
                hashed_password=Hasher.get_password_hash(user_data.password),
            )
            session.add(user)
            await session.commit()
            print(f"\nПользователь '{user.name}' успешно создан.")
    except IntegrityError as e:
        if 'unique' in str(e.orig).lower() or '23505' in str(e.orig):
            print(f"\nПользователь с email '{user_data.email}' уже существует.")
        else:
            print(f"\nОшибка базы данных: {e}")


if __name__ == "__main__":
    asyncio.run(create_user())
