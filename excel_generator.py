import pandas as pd
from app.utils.logger import logger

def generate_excel(data, output_stream):
    if not data:
        logger.warning("Nenhum dado para exportar")
        return
    df = pd.DataFrame(data)
    df.rename(columns=lambda c: c.replace("_", "").title(), inplace=True)
    df = df[df['Perguntadescricao'].notna()]
    df = df[~df['Perguntadescricao'].str.contains('Evidências:', na=False)]
    pivot_df = df.pivot_table(
        index=['Tarefaid','Recursonome','Local'],
        columns='Perguntadescricao',
        values='Conteudo',
        aggfunc='first'
    ).reset_index()
    pivot_df = pivot_df.drop(columns=['Tarefaid'])
    pivot_df = pivot_df.rename(columns={'Recursonome': 'Vistoriador'})
    pivot_df.to_excel(output_stream, index=False)
    logger.info("Excel gerado")
