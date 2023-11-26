from fastapi import APIRouter, Depends, status
from app.schemas import User, UserId, ShowUser, UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import user
from app.oauth import get_current_user

router = APIRouter(
    prefix="/usuario",
    tags= ["Usuarios"]
)

@router.get('/bienvenida')
def bienvenida():
    return {"Mensaje": "Bienvenido a tu primera api"}

@router.get('/all', response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def obtenerTodos(db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user.obtener_usuarios(db)

@router.get('/obtener/{user_id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def obtener(user_id:int, db:Session = Depends(get_db)):
    return user.obtener_usuario(user_id, db)

@router.post('/crear', status_code=status.HTTP_201_CREATED)
def crear(usuario:User, db:Session = Depends(get_db)):
    return user.crear_usuario(usuario, db)

@router.delete('/eliminar', status_code=status.HTTP_200_OK)
def eliminarUsuario(user_id:UserId, db:Session = Depends(get_db)):
    return user.eliminar_usuario(user_id, db)


@router.patch('/actualizar/{user_id}', status_code=status.HTTP_200_OK)
def actualizarUsuario(user_id:int, updateUsuario:UpdateUser, db:Session = Depends(get_db)):
    return user.actualizar_usuario(user_id, updateUsuario, db)
    