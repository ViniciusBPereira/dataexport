from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from app.utils.logger import logger
from app.services.api_consumer import run_pipeline
from app.services.excel_generator import generate_excel
import io

app = FastAPI(title="DataExport")

@app.get("/healthz")
def healthz():
    logger.info("Health check OK")
    return {"status": "ok"}

@app.get("/data_export")
def gerar_excel():
    try:
        logger.info("Iniciando exportacao…")
        data = run_pipeline()
        output = io.BytesIO()
        generate_excel(data, output)
        output.seek(0)
        logger.info("Exportacao concluida")
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=dados.xlsx"}
        )
    except Exception as e:
        logger.exception(f"Erro ao gerar Excel: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar Excel")
