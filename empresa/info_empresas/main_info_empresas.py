import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Carregar .env
load_dotenv()
ROOT = os.getenv('ROOT')

# Definição dos caminhos
PATH_ROOT = os.path.abspath(os.path.join(ROOT))
SCRIPTS_PUBLIC_PATH = os.path.abspath(os.path.join(ROOT, 'scripts_public'))
CURRENT_DIR = os.path.abspath(os.path.join(ROOT, 'empresa', 'info_empresas'))
SCRIPTS_PATH = os.path.abspath(os.path.join(CURRENT_DIR, 'scripts'))
DIRETORIO_ARQUIVOS_FINALIZADOS = os.path.abspath(os.path.join(CURRENT_DIR, 'step_3_data_processed'))

STEP_1_DATA_RAW = os.path.abspath(os.path.join(CURRENT_DIR, 'step_1_data_raw'))
STEP_2_STAGE_AREA = os.path.abspath(os.path.join(CURRENT_DIR, 'step_2_stage_area'))
STEP_3_DATA_PROCESSED = os.path.abspath(os.path.join(CURRENT_DIR, 'step_3_data_processed'))

# Adicionar caminhos ao sys.path
sys.path.append(PATH_ROOT)
sys.path.append(SCRIPTS_PUBLIC_PATH)
sys.path.append(SCRIPTS_PATH)

# Importar módulos necessários
from scripts_public.scripts_public import baixar_e_juntar_arquivos
from scripts_public.processar_excel import processar_excel
from scripts_public.apagar_arquivos_pasta import apagar_arquivos_pasta
from scripts_public.copiar_arquivos_finalizados_para_dwpii import copiar_arquivos_finalizados_para_dwpii

def main_info_empresas_baixar(driver):
    """
    Baixa e processa informações de empresas do SRInfo.
    
    Args:
        driver: Instância do WebDriver
    """
    # Garantir que as pastas existam
    os.makedirs(STEP_1_DATA_RAW, exist_ok=True)
    os.makedirs(STEP_2_STAGE_AREA, exist_ok=True)
    os.makedirs(STEP_3_DATA_PROCESSED, exist_ok=True)
    
    # Limpar as pastas
    print("Limpando pastas de dados...")
    apagar_arquivos_pasta(STEP_1_DATA_RAW)
    apagar_arquivos_pasta(STEP_2_STAGE_AREA)
    apagar_arquivos_pasta(STEP_3_DATA_PROCESSED)
    
    # Baixar dados
    print("Baixando informações de empresas...")
    link = 'https://srinfo.embrapii.org.br/company/list/'
    nome_arquivo = 'info_empresas'
    baixar_e_juntar_arquivos(driver, link, CURRENT_DIR, nome_arquivo)
    
    # Processar dados
    print("Processando dados de empresas...")
    processar_dados_empresas()

def main_info_empresas_processar():
    agregar_dados_porte_empresa()
    copiar_arquivos_finalizados_para_dwpii(DIRETORIO_ARQUIVOS_FINALIZADOS)


def agregar_dados_porte_empresa():
    """
    Agrega dados de porte das empresas ao arquivo de informações de empresas.
    """
    print("Agregando dados de porte das empresas...")
    
    path_empresas = os.path.join(ROOT, 'empresa', 'info_empresas', 'step_3_data_processed', 'info_empresas.xlsx')
    path_porte = os.path.join(ROOT, 'projeto', 'projetos_empresas', 'step_3_data_processed', 'informacoes_empresas.xlsx')
    
    # Verificar se os arquivos existem
    if not os.path.exists(path_empresas):
        print(f"ERRO: Arquivo de empresas não encontrado: {path_empresas}")
        return
    
    try:
        # Carregar dados de empresas
        print(f"Carregando dados de empresas de: {path_empresas}")
        df_empresas = pd.read_excel(path_empresas)
        
        # Verificar se o arquivo de porte existe
        if os.path.exists(path_porte):
            print(f"Carregando dados de porte de: {path_porte}")
            df_porte = pd.read_excel(path_porte)
            
            # Código comentado para futura implementação
            # colunas_remover = [
            #     'Código',
            #     'CNAE',
            #     'Empresas',
            #     'CNAE_parte',
            #     'cnae_divisao',
            # ]
            # df_porte = df_porte.drop(columns=colunas_remover)
            # 
            # df_empresas = df_empresas.merge(df_porte, left_on='cnpj', right_on='CNPJ', how='left')
            # colunas_remover = [
            #     'CNPJ',
            # ]
            # df_empresas = df_empresas.drop(columns=colunas_remover)
            # 
            # novos_nomes = {
            #     'Faixa de faturamento declarada':'faixa_faturamento',
            #     'Faixa de empregados declarada':'faixa_empregados',
            # }
            # df_empresas = df_empresas.rename(columns=novos_nomes)
        else:
            print(f"AVISO: Arquivo de porte não encontrado: {path_porte}")
            print("Continuando apenas com os dados de empresas...")
        
        # Remover duplicatas
        print("Removendo duplicatas baseadas no CNPJ...")
        df_empresas = df_empresas.drop_duplicates(subset='cnpj')
        print(f"Total de {len(df_empresas)} empresas únicas")
        
        # Salvar arquivo processado
        path_destino = os.path.join(ROOT, 'empresa', 'info_empresas', 'step_3_data_processed', 'info_empresas.xlsx')
        print(f"Salvando arquivo processado em: {path_destino}")
        
        # Garantir que o diretório de destino existe
        os.makedirs(os.path.dirname(path_destino), exist_ok=True)
        
        df_empresas.to_excel(path_destino, index=False)
        print("Arquivo salvo com sucesso")
        
    except Exception as e:
        print(f"ERRO durante o processamento dos dados de empresas: {e}")



# Definições dos caminhos e nomes de arquivos
origem = os.path.join(ROOT, 'empresa', 'info_empresas', 'step_2_stage_area')
destino = os.path.join(ROOT, 'empresa', 'info_empresas', 'step_3_data_processed')
nome_arquivo = "info_empresas.xlsx"
arquivo_origem = os.path.join(origem, nome_arquivo)
arquivo_destino = os.path.join(destino, nome_arquivo)

# Campos de interesse e novos nomes das colunas
campos_interesse = [
    'CNPJ',
    'Situação',
    'Status',
    'Tipo',
    'Natureza legal',
    'Data de abertura',
    'Nome da empresa',
    'Nome fantasia',
    'CNAE',
    'Atribuição',
    'Estado',
    'Município',
    'CEP',
    'Bairro',
    'Logradouro',
    'Número',
    'Complemento',
    'E-mail',
    'Pessoa Responsável',
    'Situação Especial',
    'Motivo para a situação',
    'Data da Situação Especial',
]

novos_nomes_e_ordem = {
    'CNPJ':'cnpj',
    'Situação':'situacao_cnpj',
    'Status':'status',
    'Tipo':'hierarquia',
    'Natureza legal':'natureza_legal',
    'Data de abertura':'data_abertura',
    'Nome da empresa':'razao_social',
    'Nome fantasia':'nome_fantasia',
    'CNAE':'cnae_principal',
    'Atribuição':'cnae_descricao',
    'Estado':'endereco_uf',
    'Município':'endereco_municipio',
    'CEP':'endereco_cep',
    'Bairro':'endereco_bairro',
    'Logradouro':'endereco_logradouro',
    'Número':'endereco_numero',
    'Complemento':'endereco_complemento',
    'E-mail':'contato_email',
    'Pessoa Responsável':'pessoa_responsavel',
    'Situação Especial':'recuperacao_judicial',
    'Motivo para a situação':'recuperacao_judicial_motivo',
    'Data da Situação Especial':'recuperacao_judicial_data',
}


def processar_dados_empresas():
    """
    Processa os dados brutos de empresas, selecionando campos de interesse e renomeando colunas.
    """
    print("Processando dados brutos de empresas...")
    
    # Verificar se o arquivo de origem existe
    if not os.path.exists(arquivo_origem):
        print(f"ERRO: Arquivo de origem não encontrado: {arquivo_origem}")
        print("Verifique se o download e a junção dos arquivos foram realizados corretamente.")
        return
    
    try:
        # Garantir que o diretório de destino existe
        os.makedirs(os.path.dirname(arquivo_destino), exist_ok=True)
        
        # Processar o arquivo
        print(f"Processando arquivo: {arquivo_origem}")
        processar_excel(arquivo_origem, campos_interesse, novos_nomes_e_ordem, arquivo_destino)
        print(f"Arquivo processado e salvo em: {arquivo_destino}")
    
    except Exception as e:
        print(f"ERRO durante o processamento do arquivo: {e}")
