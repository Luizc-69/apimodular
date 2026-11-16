from fastapi import APIRouter, HTTPException
from app.schemas.registro import RegistroBase, RegistroResponse
from app.repositories import registro as registro_repo

router = APIRouter(prefix="/registros", tags=["Registros"])

@router.post("", response_model=RegistroResponse, status_code=201)
def criar_registro(registro: RegistroBase):
    if not registro.titulo.strip():
        raise HTTPException(status_code=400, detail="O título não pode estar em branco.")
    try:
        novo_id = registro_repo.criar(registro)
        return {**registro.model_dump(), "id": novo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")

@router.get("", response_model=list[RegistroResponse], status_code=200)
def listar_registros():
    return registro_repo.listar_todos()

@router.get("/{registro_id}", response_model=RegistroResponse, status_code=200)
def buscar_registro(registro_id: int):
    registro = registro_repo.buscar_por_id(registro_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    return registro

@router.put("/{registro_id}", response_model=RegistroResponse, status_code=200)
def atualizar_registro(registro_id: int, registro: RegistroBase):
    try:
        atualizado = registro_repo.atualizar(registro_id, registro)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Registro não encontrado para atualização.")
        return {**registro.model_dump(), "id": registro_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{registro_id}", status_code=200)
def deletar_registro(registro_id: int):
    deletado = registro_repo.deletar(registro_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Registro não encontrado para exclusão.")
    return {"mensagem": "Registro removido com sucesso."}
