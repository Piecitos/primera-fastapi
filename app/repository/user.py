from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash

def crear_usuario(usuario, db:Session):
    usuarioFormat = usuario.dict()
    try:
        password_hash = Hash.hash_password(usuarioFormat['password'])
        nuevo_usuario = models.User(
            username=usuarioFormat['username'],
            password=password_hash,
            nombre=usuarioFormat['nombre'],
            apellido=usuarioFormat['apellido'],
            direccion=usuarioFormat['direccion'],
            telefono=usuarioFormat['telefono'],
            correo=usuarioFormat['correo']
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {"respuesta" : "Usuario creado correctamente"}
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error creando usuario {e}"
        )

def obtener_usuarios(db:Session):
    return db.query(models.User).all()

def obtener_usuario(user_id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No existe el usuario con el id {user_id}"
        )
    return usuario

def eliminar_usuario(user_id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id.id)
    if not usuario.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No existe el usuario con el id {user_id.id}"
        )
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta" : "Usuario eliminado correctamente"}

def actualizar_usuario(user_id, updateUsuario, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No existe el usuario con el id {user_id}"
        )
    
    try:
        if updateUsuario.password:
            password_hash = Hash.hash_password(updateUsuario.password)
            updateUsuario.password = password_hash

        usuario.update(updateUsuario.dict(exclude_unset=True))
        db.commit()
        return {"respuesta" : "Usuario actualizado correctamente"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error actualizando usuario {e}"
        )
    