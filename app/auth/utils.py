from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta
from db.database import db_client
from models.user import UserDB,User,UserCreate
from schemas.user import user_db_schema,user_schema


# Hash algoritm
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 15
SECRET = "1caca100a97562784de56305487b20a74c7f7a1b5de0583f93c6cde99b053aeb"


oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

crypt = CryptContext(schemes=["bcrypt"])


router = APIRouter()

# SEARCH
async def search_user(field: str, key: str):
    try:
        user = db_client.local.users.find_one({field: key})
        if user:
            return UserDB(**user_db_schema(user))
    except Exception as e:
        print(f"Error: {e}")
        return None



async def autenticate_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=401, detail="Credenciales invalidas")
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    return await search_user("username", username)


async def current_user(user: User = Depends(autenticate_user)):
    if user.disabled:
        raise HTTPException(status_code=401, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await search_user("username", form.username)
    if not user:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {"sub": user.username, "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}



@router.get("/users/me")
async def me(user:User = Depends(current_user)):   # esta funcion DEPENDE que este autenticado, por eso usamos el DEPENDS()
    return user





## CRUD

@router.post("/users/create", response_model=User)
async def create_user(user: UserCreate):
    existing_user = await search_user("email", user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    
    user_dict = user.dict()
    user_dict["password"] = crypt.hash(user.password)  # Hash the password
    user_dict["disabled"] = False  # Ensure the disabled field is set

    try:
        result = db_client.local.users.insert_one(user_dict)
        new_user = db_client.local.users.find_one({"_id": result.inserted_id})
        return User(**user_schema(new_user))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear el usuario")
