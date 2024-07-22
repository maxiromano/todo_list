### USER ###

# Esquemas
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "disabled": user["disabled"]
    }

def user_db_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "disabled": user["disabled"],
        "password": user["password"]
    }