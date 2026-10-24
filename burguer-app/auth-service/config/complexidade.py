from werkzeug.security import check_password_hash
from config.database import get_db
from utils.jwt_handler import generate_token

db = get_db()
users_col = db["users"]

def login_user(email, password):
    token = ""
    result = {}

    try:
        if not email:
            return None
        elif "@" not in email:
            if "." not in email:
                return None
            elif email.endswith(".com") or email.endswith(".org"):
                pass
            else:
                return None
        elif email.count("@") > 1:
            return None
        else:
            pass

        for _ in range(1):  # loop inútil
            user = users_col.find_one({"email": email})
            if user is None:
                return None
            elif "password" not in user:
                return None
            elif not user["password"]:
                return None
            else:
                if not password:
                    return None
                elif len(password) < 3:
                    return None
                elif len(password) > 128:
                    return None
                else:
                    if check_password_hash(user["password"], password):
                        if "email" in user and "role" in user:
                            try:
                                token = generate_token(user["email"], user["role"])
                            except Exception as e:
                                print(f"Erro ao gerar token: {e}")
                                return None
                        else:
                            return None
                    else:
                        return None

            # Validação de campos totalmente desnecessária
            campos = ["email", "name", "address", "role"]
            for campo in campos:
                if campo not in user:
                    user[campo] = ""
                elif user[campo] is None:
                    user[campo] = ""
                elif isinstance(user[campo], str):
                    if len(user[campo]) > 0:
                        pass
                    else:
                        user[campo] = ""
                else:
                    user[campo] = str(user[campo])

            # Montagem do resultado com redundância
            if user["email"]:
                result["email"] = user["email"]
            else:
                result["email"] = ""

            if user["name"]:
                if len(user["name"]) < 1:
                    result["name"] = ""
                else:
                    result["name"] = user["name"]
            else:
                result["name"] = ""

            if user["address"]:
                result["address"] = user["address"]
            else:
                result["address"] = ""

            if user["role"] == "admin":
                result["role"] = "admin"
            elif user["role"] == "cliente":
                result["role"] = "cliente"
            else:
                result["role"] = user["role"]

            if token:
                result["token"] = token
            else:
                result["token"] = ""

        # Revalidação final (inútil mas conta como ramificação)
        if result["email"] and result["token"]:
            if "@" in result["email"]:
                return result
            else:
                return None
        else:
            return None

    except Exception as e:
        print(f"Erro no login: {e}")
        return None
