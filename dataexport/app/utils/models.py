from pydantic import BaseModel
from typing import Optional

class Tarefa(BaseModel):
    Id: str
    Local: str

class Checklist(BaseModel):
    tarefaId: str
    local: str
    data: Optional[str]
    recursonome: Optional[str]
    perguntadescricao: Optional[str]
    conteudo: Optional[str]