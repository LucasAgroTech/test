# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from os import path

block_cipher = None

# Diretório raiz do projeto
root_dir = path.abspath(path.dirname(__file__))

# Arquivos de dados adicionais
added_files = [
    ('README.md', '.'),
    ('README_PACKAGED.md', '.'),
    ('.env', '.'),
    ('create_icon.py', '.'),
]

# Coletar todos os módulos necessários
a = Analysis(
    ['gui_main.py'],  # Ponto de entrada com GUI
    pathex=[root_dir],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'pandas', 
        'selenium', 
        'office365', 
        'pyautogui', 
        'pyshorteners', 
        'python-dotenv', 
        'psutil',
        'PyQt5',
        'webdriver_manager',
        'empresa.info_empresas.main_info_empresas',
        'analises_relatorios.empresas_contratantes.main_empresas_contratantes',
        'analises_relatorios.projetos_contratados.main_projetos_contratados',
        'projeto.contratos.main_contratos',
        'projeto.projetos.main_projetos',
        'projeto.projetos_empresas.main_projetos_empresas',
        'projeto.estudantes.main_estudantes',
        'projeto.pedidos_pi.main_pedidos_pi',
        'projeto.macroentregas.main_macroentregas',
        'projeto.sebrae.main_sebrae',
        'projeto.classificacao_projeto.main_classificacao_projeto',
        'projeto.portfolio.main_portfolio',
        'prospeccao.comunicacao.main_comunicacao',
        'prospeccao.eventos_srinfo.main_eventos_srinfo',
        'prospeccao.prospeccao.main_prospeccao',
        'negociacoes.negociacoes.main_negociacoes',
        'negociacoes.planos_trabalho.main_planos_trabalho',
        'negociacoes.propostas_tecnicas.main_propostas_tecnicas',
        'unidade_embrapii.info_unidades.main_info_unidades',
        'unidade_embrapii.equipe_ue.main_equipe_ue',
        'unidade_embrapii.termos_cooperacao.main_termos_cooperacao',
        'unidade_embrapii.plano_acao.main_plano_acao',
        'unidade_embrapii.plano_metas.main_plano_metas',
        'scripts_public.registrar_log',
        'scripts_public.levar_arquivos_sharepoint',
        'scripts_public.comparar_excel',
        'scripts_public.whatsapp',
        'scripts_public.report_snapshot',
        'scripts_public.webdriver',
        'scripts_public.buscar_arquivos_sharepoint',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Criar ícone se não existir
icon_path = None
if os.path.exists('pipeline_icon.ico'):
    icon_path = 'pipeline_icon.ico'
else:
    try:
        from create_icon import create_icon
        icon_path = create_icon()
    except:
        print("Aviso: Não foi possível criar o ícone. O executável será gerado sem ícone.")

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pipeline EMBRAPII SRInfo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # True para mostrar console durante o desenvolvimento, mudar para False na versão final
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pipeline_embrapii_srinfo',
)
