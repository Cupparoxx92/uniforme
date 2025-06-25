from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent / "data"
BASE.mkdir(exist_ok=True)

def _ensure_file(path: Path, header: str):
    if not path.exists():
        path.write_text(header + "\n", encoding="utf-8")

# Arquivos
COLAB  = BASE / "colaboradores.csv"
PEDIDO = BASE / "pedidos.csv"
ESTOQUE = BASE / "estoque.csv"

_ensure_file(COLAB, "Matricula,Nome,Funcao,Setor,Genero,UltimoPeriodico")
_ensure_file(PEDIDO, "Timestamp,Matricula,Nome,TipoPedido,Itens,Justificativa,Status")
_ensure_file(ESTOQUE, "Item,Tamanho,Saldo")

# ------------ API simples -----------------
def load_colaboradores() -> pd.DataFrame:
    return pd.read_csv(COLAB)

def save_colaboradores(df: pd.DataFrame):
    df.to_csv(COLAB, index=False)

def append_pedido(row: dict):
    pd.DataFrame([row]).to_csv(PEDIDO, mode="a", header=False, index=False)

