from pydantic import BaseModel, EmailStr

class UsuarioEntrada(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    sexo: str
    telefone: int | None = None
    foto: str | None = None

class InstrutorEntrada(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: int
    administrador: bool

class ExercicioEntrada(BaseModel):
    nome: str
    grupo: str
    imagem: str
    video: str | None = None

class SerieEntrada(BaseModel):
    numero: int
    peso: float 
    id_exercicio: int

class TreinoEntrada(BaseModel):
    nome: str
    objetivo: str
    descricao: str

class PlanoEntrada(BaseModel):
    nome: str
    valor: float
    descricao: str
    duracao: int

class MatriculaEntrada(BaseModel):
    id_usuario: int
    id_plano: int
    status: str


class AlterarPerfil(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
    telefone: str | None = None
    sexo: str | None = None
    foto: str | None = None

class AlterarTreino(BaseModel):
    nome: str | None = None
    objetivo: str | None = None
    descricao: str | None = None