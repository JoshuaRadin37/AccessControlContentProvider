from random import randint

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_db(app):
    global db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def reset_database(app):
    global db
    with app.app_context():
        db.drop_all()
        db.create_all()


token_length = 48


def __generate_access_code():
    code = ""
    checksum = 0
    for _ in range(0, token_length):
        initial = randint(0, 25)  # A-Z and 0-9
        checksum += initial
        next = chr(ord('A') + initial)
        code += next

    checksum %= 26
    print("Checksum val:", checksum)

    next = chr(ord('A') + checksum)
    print("Initial Checksum:", ord(next))
    code += next
    if not check_checksum(code):
        raise RuntimeError("Checksum created invalid based on own rules")
    return code


# Generates an access control token, and returns the string
def generate_token(app, owner_id, valid_domain, expiration_date, start_date=None):
    from models import AccessToken
    with app.app_context():
        while True:
            access_code = __generate_access_code()
            if AccessToken.query.filter_by(code=access_code).first() is None:
                break

        if start_date is None:
            token = AccessToken(code=access_code, owner_id=owner_id, valid_domain=valid_domain, time_end=expiration_date)
        else:
            token = AccessToken(code=access_code, owner_id=owner_id, valid_domain=valid_domain, time_start=start_date, time_end=expiration_date)
        db.session.add(token)
        db.session.commit()
        return access_code


# Checks if the access code is valid by checking it's checksum
def check_checksum(code: str) -> bool:
    checksum = 0
    print("checking", code)
    for i in range(0, token_length):
        char = code[i]
        print("char", i, "is", char)
        if char.isalpha():
            next = ord(char) - ord('A')
        else:
            raise RuntimeError("Invalid character in checksum")
        print("next =", next)
        checksum += next

    original = code[token_length]
    checksum %= 26

    next = chr(ord('A') + checksum)

    print('Original: ', ord(original))
    print('Found: ', ord(next))
    return original == next
