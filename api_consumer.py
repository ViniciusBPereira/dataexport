import os
import json
import requests
from typing import List, Dict

from logger import logger
from models import Tarefa, Checklist


# === Configurações ===
API_TOKEN = os.getenv("API_TOKEN")  # nunca hardcode token
if not API_TOKEN:
    raise RuntimeError("API_TOKEN não configurado no ambiente!")

URL_TAREFAS = "https://apiprod.gpsvista.com.br/api/planejamento/grid/tarefas?StatusFinalizada=true&Disponibilizacao_yyyyMM=2025-08"
URL_CHECKLIST = "https://apiprod.gpsvista.com.br/api/operacao/listar-por-tarefaId?tarefaId={}"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

PAYLOAD = {
    "value": {
        "requiresCounts": True,
        "where": [
            {
                "isComplex": True,
                "ignoreAccent": False,
                "condition": "and",
                "predicates": [
                    {"isComplex": False, "field": "CR", "operator": "contains", "value": "80035", "ignoreCase": True, "ignoreAccent": False},
                    {"isComplex": False, "field": "Nome", "operator": "contains", "value": "INSPEÇÃO DE EXTINTORES", "ignoreCase": True, "ignoreAccent": False}
                ]
            }
        ],
        "sorted": [{"name": "Numero", "direction": "descending"}]
    }
}


# === Funções principais ===
def fetch_tarefas() -> List[Tarefa]:
    """Busca a lista de tarefas via API."""
    logger.info("Buscando tarefas...")
    try:
        resp = requests.post(URL_TAREFAS, headers=HEADERS, json=PAYLOAD, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        tarefas = [Tarefa(**item) for item in data.get("result", [])]
        logger.info(f"{len(tarefas)} tarefas recebidas.")
        return tarefas
    except Exception:
        logger.error("Erro ao buscar tarefas", exc_info=True)
        return []


def fetch_checklist(tarefas: List[Tarefa]) -> List[Dict]:
    """Busca os checklists das tarefas recebidas."""
    resultados: List[Checklist] = []

    for t in tarefas:
        url = URL_CHECKLIST.format(t.Id)
        logger.info(f"Buscando checklist da tarefa {t.Id} ({t.Local})...")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            checklist_items = resp.json()

            for item in checklist_items:
                resultados.append(Checklist(
                    tarefaId=t.Id,
                    local=t.Local,
                    data=item.get("data"),
                    recursonome=item.get("recursonome"),
                    perguntadescricao=item.get("perguntadescricao"),
                    conteudo=item.get("conteudo")
                ))
        except Exception:
            logger.error(f"Erro ao buscar checklist da tarefa {t.Id}", exc_info=True)

    return [r.dict() for r in resultados]


def run_pipeline() -> List[Dict]:
    """Executa o fluxo completo: tarefas -> checklists -> JSON final."""
    tarefas = fetch_tarefas()
    if not tarefas:
        logger.warning("Nenhuma tarefa encontrada.")
        return []
    return fetch_checklist(tarefas)

