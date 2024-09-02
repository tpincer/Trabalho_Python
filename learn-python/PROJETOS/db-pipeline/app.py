import sqlite3
import os
import pandas as pd
from dotenv import load_dotenv
import assets.utils as utils
from assets.utils import logger
import datetime

load_dotenv()

def data_clean(df, metadados):
    '''
    Função principal para saneamento dos dados
    INPUT: Pandas DataFrame, dicionário de metadados
    OUTPUT: Pandas DataFrame, base tratada
    '''
    logger.info(f'Iniciando o saneamento dos dados; {datetime.datetime.now()}')

    df["data_voo"] = pd.to_datetime(df[['year', 'month', 'day']]) 
    logger.info('Data de voo criada a partir das colunas year, month, day.')

    df = utils.null_exclude(df, metadados["cols_chaves"])
    logger.info('Exclusão de observações nulas concluída.')

    df = utils.convert_data_type(df, metadados["tipos_originais"])
    logger.info('Conversão de tipos de dados concluída.')

    df = utils.select_rename(df, metadados["cols_originais"], metadados["cols_renamed"])
    logger.info('Renomeação de colunas concluída.')

    df = utils.string_std(df, metadados["std_str"])
    logger.info('Padronização de strings concluída.')

    df["datetime_partida"] = df["datetime_partida"].str.replace('.0', '', regex=False)
    df["datetime_chegada"] = df["datetime_chegada"].str.replace('.0', '', regex=False)
    logger.info('Remoção de sufixos ".0" das colunas datetime_partida e datetime_chegada.')


    for col in metadados["corrige_hr"]:
        df[f'{col}_formatted'] = pd.to_datetime(df["data_voo"].astype(str) + " " + df[col].apply(utils.corrige_hora))
        logger.info(f'Correção e formatação da coluna {col} concluída.')

    logger.info(f'Saneamento concluído; {datetime.datetime.now()}')
    return df

def feat_eng(df):
    '''
    Função para engenharia de features no DataFrame.
    INPUT:df (pd.DataFrame): DataFrame limpo e tratado.

    OUTPUT:pd.DataFrame: DataFrame com novas features adicionadas.
    '''
    logger.info("Iniciando engenharia de features")
    
    # Especificar o formato de data e hora para evitar avisos e melhorar performance
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Certifique-se de que as colunas são do tipo datetime
    df['datetime_partida'] = pd.to_datetime(df['datetime_partida'], format=date_format, errors='coerce')
    df['datetime_chegada'] = pd.to_datetime(df['datetime_chegada'], format=date_format, errors='coerce')

    # Verifica se a conversão foi bem-sucedida
    if df['datetime_partida'].isnull().any() or df['datetime_chegada'].isnull().any():
        logger.warning("Algumas datas não puderam ser convertidas para datetime")

    # Calcular a duração do voo em horas
    df['flight_duration_hours'] = (df['datetime_chegada'] - df['datetime_partida']).dt.total_seconds() / 3600
    
    logger.info("Engenharia de features concluída")
    return df



def save_data_sqlite(df):
    try:
        conn = sqlite3.connect("data/NyflightsDB.db")
        logger.info(f'Conexão com banco estabelecida ; {datetime.datetime.now()}')
    except:
        logger.error(f'Problema na conexão com banco; {datetime.datetime.now()}')
    c = conn.cursor()
    df.to_sql('nyflights', con=conn, if_exists='replace')
    conn.commit()
    logger.info(f'Dados salvos com sucesso; {datetime.datetime.now()}')
    conn.close()

def fetch_sqlite_data(table):
    try:
        conn = sqlite3.connect("data/NyflightsDB.db")
        logger.info(f'Conexão com banco estabelecida ; {datetime.datetime.now()}')
    except:
        logger.error(f'Problema na conexão com banco; {datetime.datetime.now()}')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table} LIMIT 5")
    print(c.fetchall())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    logger.info(f'Início da execução ; {datetime.datetime.now()}')
    
    # Carregar os metadados e dados
    metadados = utils.read_metadado(os.getenv('META_PATH'))
    df = pd.read_csv(os.getenv('DATA_PATH'), index_col=0)
    
    # Saneamento dos dados
    df = data_clean(df, metadados)
    print(df.head())
    
    # Validação dos dados
    utils.null_check(df, metadados["null_tolerance"])
    utils.keys_check(df, metadados["cols_chaves"])
    
    # Engenharia de Features
    df = feat_eng(df)
    
    # Salvar dados no SQLite
    save_data_sqlite(df)
    
    # Consultar e exibir dados do banco
    fetch_sqlite_data(metadados["tabela"][0])
    
    logger.info(f'Fim da execução ; {datetime.datetime.now()}')