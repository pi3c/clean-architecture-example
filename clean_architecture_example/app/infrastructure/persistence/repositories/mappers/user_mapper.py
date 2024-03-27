from app.domain.users.user import User, UserEmail, UserFirstName, UserId, UserLastName


def user_from_dict_to_entity(adict: dict) -> User:
    return User(
        id=UserId(adict["id"]),
        first_name=UserFirstName(adict["first_name"]),
        last_name=UserLastName(adict["last_name"]),
        email=UserEmail(adict["email"]),
        hashed_password=adict["hashed_password"],
    )
