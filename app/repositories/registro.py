from app.core.database import get_db_connection
from app.schemas.registro import RegistroBase

def criar(registro: RegistroBase) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO registros (titulo, descricao, ativo) VALUES (?, ?, ?)",
        (registro.titulo, registro.descricao, registro.ativo)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def listar_todos() -> list[dict]:
    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()
    return [dict(reg) for reg in registros]

def buscar_por_id(registro_id: int) -> dict | None:
    conn = get_db_connection()
    registro = conn.execute("SELECT * FROM registros WHERE id = ?", (registro_id,)).fetchone()
    conn.close()
    return dict(registro) if registro else None

def atualizar(registro_id: int, registro: RegistroBase) -> bool:
    conn = get_db_connection()
    existente = conn.execute("SELECT * FROM registros WHERE id = ?", (registro_id,)).fetchone()
    if existente is None:
        conn.close()
        return False

    conn.execute(
        "UPDATE registros SET titulo = ?, descricao = ?, ativo = ? WHERE id = ?",
        (registro.titulo, registro.descricao, registro.ativo, registro_id)
    )
    conn.commit()
    conn.close()
    return True

def deletar(registro_id: int) -> bool:
    conn = get_db_connection()
    existente = conn.execute("SELECT * FROM registros WHERE id = ?", (registro_id,)).fetchone()
    if existente is None:
        conn.close()
        return False

    conn.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
    conn.commit()
    conn.close()
    return True
