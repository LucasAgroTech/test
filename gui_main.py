import sys
import os
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QProgressBar, QTextEdit, 
                            QPushButton, QCheckBox, QGroupBox, QScrollArea,
                            QSplitter, QFrame, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor

# Importar o pipeline principal
from main import (main_pipeline_srinfo, criar_estrutura_diretorios, 
                 buscar_arquivos_sharepoint, configurar_webdriver, 
                 encerrar_webdriver, logear, duracao_tempo)

class PipelineWorker(QThread):
    """Thread worker para executar o pipeline em segundo plano"""
    progress_update = pyqtSignal(str, int)
    log_update = pyqtSignal(str)
    module_started = pyqtSignal(str)
    module_completed = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, plano_metas=False, gerar_snapshot=False, enviar_wpp=False):
        super().__init__()
        self.plano_metas = plano_metas
        self.gerar_snapshot = gerar_snapshot
        self.enviar_wpp = enviar_wpp
        self.running = True
        
    def run(self):
        try:
            inicio = datetime.now()
            self.log_update.emit(f'Início: {inicio.strftime("%d/%m/%Y %H:%M:%S")}')
            
            # Verificar e criar estrutura de diretórios
            self.log_update.emit("Verificando e criando estrutura de diretórios...")
            criar_estrutura_diretorios()
            
            # Lista de módulos para acompanhamento
            modulos = [
                'sharepoint',
                'info_empresas',
                'empresas_contratantes',
                'info_unidades',
                'equipe_ue',
                'termos_cooperacao',
                'plano_acao',
                'plano_metas',
                'sebrae',
                'projetos_contratados',
                'projetos_empresas',
                'projetos',
                'contratos',
                'estudantes',
                'pedidos_pi',
                'macroentregas',
                'comunicacao',
                'eventos_srinfo',
                'prospeccao',
                'negociacoes',
                'propostas_tecnicas',
                'planos_trabalho',
                'classificacao_projetos',
                'portfolio',
                'levar_arquivos_sharepoint',
                'report_snapshot',
                'whatsapp'
            ]
            
            # Inicializar progresso para todos os módulos
            for modulo in modulos:
                self.progress_update.emit(modulo, 0)
            
            # Executar o pipeline com callbacks para atualizar a interface
            log = []
            
            # SharePoint
            self.module_started.emit('sharepoint')
            self.log_update.emit("Buscando arquivos do SharePoint...")
            buscar_arquivos_sharepoint()
            self.progress_update.emit('sharepoint', 100)
            self.module_completed.emit('sharepoint')
            
            # Configurar o WebDriver
            self.log_update.emit("Configurando WebDriver...")
            driver = configurar_webdriver()
            
            # Importar módulos aqui para evitar importação circular
            from empresa.info_empresas.main_info_empresas import main_info_empresas_baixar, main_info_empresas_processar
            from analises_relatorios.empresas_contratantes.main_empresas_contratantes import main_empresas_contratantes
            from analises_relatorios.projetos_contratados.main_projetos_contratados import main_projetos_contratados
            from projeto.contratos.main_contratos import main_contratos
            from projeto.projetos.main_projetos import main_projetos
            from projeto.projetos_empresas.main_projetos_empresas import main_projetos_empresas
            from projeto.estudantes.main_estudantes import main_estudantes
            from projeto.pedidos_pi.main_pedidos_pi import main_pedidos_pi
            from projeto.macroentregas.main_macroentregas import main_macroentregas
            from projeto.sebrae.main_sebrae import main_sebrae
            from projeto.classificacao_projeto.main_classificacao_projeto import main_classificacao_projeto
            from projeto.portfolio.main_portfolio import main_portfolio
            from prospeccao.comunicacao.main_comunicacao import main_comunicacao
            from prospeccao.eventos_srinfo.main_eventos_srinfo import main_eventos_srinfo
            from prospeccao.prospeccao.main_prospeccao import main_prospeccao
            from negociacoes.negociacoes.main_negociacoes import main_negociacoes
            from negociacoes.planos_trabalho.main_planos_trabalho import main_planos_trabalho
            from negociacoes.propostas_tecnicas.main_propostas_tecnicas import main_propostas_tecnicas
            from unidade_embrapii.info_unidades.main_info_unidades import main_info_unidades
            from unidade_embrapii.equipe_ue.main_equipe_ue import main_equipe_ue
            from unidade_embrapii.termos_cooperacao.main_termos_cooperacao import main_termos_cooperacao
            from unidade_embrapii.plano_acao.main_plano_acao import main_plano_acao
            from unidade_embrapii.plano_metas.main_plano_metas import main_plano_metas
            from scripts_public.registrar_log import registrar_log
            from scripts_public.levar_arquivos_sharepoint import levar_arquivos_sharepoint
            from scripts_public.comparar_excel import comparar_excel
            from scripts_public.whatsapp import enviar_whatsapp
            from scripts_public.report_snapshot import gerar_report_snapshot
            
            # SEÇÃO 1/5: COLETA DE DADOS
            self.log_update.emit('SEÇÃO 1/5: COLETA DE DADOS')
            
            # Empresas
            self.log_update.emit('Subseção: Empresas')
            
            # Info Empresas
            self.module_started.emit('info_empresas')
            self.log_update.emit("Baixando informações de empresas...")
            main_info_empresas_baixar(driver)
            log = logear(log, 'info_empresas')
            self.progress_update.emit('info_empresas', 100)
            self.module_completed.emit('info_empresas')
            
            # Empresas Contratantes
            self.module_started.emit('empresas_contratantes')
            self.log_update.emit("Processando empresas contratantes...")
            main_empresas_contratantes(driver)
            log = logear(log, 'empresas_contratantes')
            self.progress_update.emit('empresas_contratantes', 100)
            self.module_completed.emit('empresas_contratantes')
            
            # Unidades Embrapii
            self.log_update.emit('Subseção: Unidades Embrapii')
            
            # Info Unidades
            self.module_started.emit('info_unidades')
            self.log_update.emit("Baixando informações de unidades...")
            main_info_unidades(driver)
            log = logear(log, 'info_unidades')
            self.progress_update.emit('info_unidades', 100)
            self.module_completed.emit('info_unidades')
            
            # Equipe UE
            self.module_started.emit('equipe_ue')
            self.log_update.emit("Processando equipe UE...")
            main_equipe_ue(driver)
            log = logear(log, 'equipe_ue')
            self.progress_update.emit('equipe_ue', 100)
            self.module_completed.emit('equipe_ue')
            
            # Termos Cooperação
            self.module_started.emit('termos_cooperacao')
            self.log_update.emit("Processando termos de cooperação...")
            main_termos_cooperacao(driver)
            log = logear(log, 'ue_termos_cooperacao')
            self.progress_update.emit('termos_cooperacao', 100)
            self.module_completed.emit('termos_cooperacao')
            
            # Plano Ação
            self.module_started.emit('plano_acao')
            self.log_update.emit("Processando plano de ação...")
            main_plano_acao(driver)
            log = logear(log, 'ue_termos_cooperacao')
            self.progress_update.emit('plano_acao', 100)
            self.module_completed.emit('plano_acao')
            
            # Plano Metas (opcional)
            if self.plano_metas:
                self.module_started.emit('plano_metas')
                self.log_update.emit("Processando plano de metas...")
                main_plano_metas(driver)
                log = logear(log, 'ue_plano_metas')
                self.progress_update.emit('plano_metas', 100)
                self.module_completed.emit('plano_metas')
            else:
                self.progress_update.emit('plano_metas', 0)
                self.log_update.emit("Plano de metas ignorado (opcional).")
            
            # Projetos
            self.log_update.emit('Subseção: Projetos')
            
            # Sebrae
            self.module_started.emit('sebrae')
            self.log_update.emit("Processando dados do Sebrae...")
            main_sebrae(driver)
            log = logear(log, 'sebrae')
            self.progress_update.emit('sebrae', 100)
            self.module_completed.emit('sebrae')
            
            # Projetos Contratados
            self.module_started.emit('projetos_contratados')
            self.log_update.emit("Processando projetos contratados...")
            main_projetos_contratados(driver)
            log = logear(log, 'projetos_contratados')
            self.progress_update.emit('projetos_contratados', 100)
            self.module_completed.emit('projetos_contratados')
            
            # Projetos Empresas
            self.module_started.emit('projetos_empresas')
            self.log_update.emit("Processando projetos de empresas...")
            main_projetos_empresas()
            log = logear(log, 'projetos_empresas')
            self.progress_update.emit('projetos_empresas', 100)
            self.module_completed.emit('projetos_empresas')
            
            # Projetos
            self.module_started.emit('projetos')
            self.log_update.emit("Processando projetos...")
            main_projetos(driver)
            log = logear(log, 'projetos')
            self.progress_update.emit('projetos', 100)
            self.module_completed.emit('projetos')
            
            # Contratos
            self.module_started.emit('contratos')
            self.log_update.emit("Processando contratos...")
            main_contratos(driver)
            log = logear(log, 'contratos')
            self.progress_update.emit('contratos', 100)
            self.module_completed.emit('contratos')
            
            # Estudantes
            self.module_started.emit('estudantes')
            self.log_update.emit("Processando estudantes...")
            main_estudantes(driver)
            log = logear(log, 'estudantes')
            self.progress_update.emit('estudantes', 100)
            self.module_completed.emit('estudantes')
            
            # Pedidos PI
            self.module_started.emit('pedidos_pi')
            self.log_update.emit("Processando pedidos PI...")
            main_pedidos_pi(driver)
            log = logear(log, 'pedidos_pi')
            self.progress_update.emit('pedidos_pi', 100)
            self.module_completed.emit('pedidos_pi')
            
            # Macroentregas
            self.module_started.emit('macroentregas')
            self.log_update.emit("Processando macroentregas...")
            main_macroentregas(driver)
            log = logear(log, 'macroentregas')
            self.progress_update.emit('macroentregas', 100)
            self.module_completed.emit('macroentregas')
            
            # Comunicação
            self.module_started.emit('comunicacao')
            self.log_update.emit("Processando comunicação...")
            main_comunicacao(driver)
            log = logear(log, 'comunicacao')
            self.progress_update.emit('comunicacao', 100)
            self.module_completed.emit('comunicacao')
            
            # Eventos SRInfo
            self.module_started.emit('eventos_srinfo')
            self.log_update.emit("Processando eventos SRInfo...")
            main_eventos_srinfo(driver)
            log = logear(log, 'eventos_srinfo')
            self.progress_update.emit('eventos_srinfo', 100)
            self.module_completed.emit('eventos_srinfo')
            
            # Prospecção
            self.module_started.emit('prospeccao')
            self.log_update.emit("Processando prospecção...")
            main_prospeccao(driver)
            log = logear(log, 'prospeccao')
            self.progress_update.emit('prospeccao', 100)
            self.module_completed.emit('prospeccao')
            
            # Negociações
            self.module_started.emit('negociacoes')
            self.log_update.emit("Processando negociações...")
            main_negociacoes(driver)
            log = logear(log, 'negociacoes')
            self.progress_update.emit('negociacoes', 100)
            self.module_completed.emit('negociacoes')
            
            # Propostas Técnicas
            self.module_started.emit('propostas_tecnicas')
            self.log_update.emit("Processando propostas técnicas...")
            main_propostas_tecnicas(driver)
            log = logear(log, 'propostas_tecnicas')
            self.progress_update.emit('propostas_tecnicas', 100)
            self.module_completed.emit('propostas_tecnicas')
            
            # Planos Trabalho
            self.module_started.emit('planos_trabalho')
            self.log_update.emit("Processando planos de trabalho...")
            main_planos_trabalho(driver)
            log = logear(log, 'planos_trabalho')
            self.progress_update.emit('planos_trabalho', 100)
            self.module_completed.emit('planos_trabalho')
            
            # Encerrar WebDriver
            self.log_update.emit("Encerrando WebDriver...")
            encerrar_webdriver(driver)
            
            # SEÇÃO 2/5: PROCESSAMENTO DE DADOS
            self.log_update.emit('SEÇÃO 2/5: PROCESSAMENTO DE DADOS')
            
            # Classificação Projetos
            self.module_started.emit('classificacao_projetos')
            self.log_update.emit("Processando classificação de projetos...")
            main_classificacao_projeto()
            log = logear(log, 'classificacao_projetos')
            self.progress_update.emit('classificacao_projetos', 100)
            self.module_completed.emit('classificacao_projetos')
            
            # Info Empresas Processar
            self.log_update.emit("Processando informações de empresas...")
            main_info_empresas_processar()
            log = logear(log, 'info_empresas')
            
            # Portfolio
            self.module_started.emit('portfolio')
            self.log_update.emit("Processando portfolio...")
            main_portfolio()
            log = logear(log, 'portfolio')
            self.progress_update.emit('portfolio', 100)
            self.module_completed.emit('portfolio')
            
            # Registrar Log
            self.log_update.emit("Registrando logs...")
            registrar_log(log)
            
            # SEÇÃO 3/5: LEVAR ARQUIVOS PARA O SHAREPOINT
            self.log_update.emit('SEÇÃO 3/5: LEVAR ARQUIVOS PARA O SHAREPOINT')
            
            # Levar Arquivos SharePoint
            self.module_started.emit('levar_arquivos_sharepoint')
            self.log_update.emit("Enviando arquivos para o SharePoint...")
            levar_arquivos_sharepoint()
            self.progress_update.emit('levar_arquivos_sharepoint', 100)
            self.module_completed.emit('levar_arquivos_sharepoint')
            
            # SEÇÃO 4/5: GERAR SNAPSHOT (opcional)
            if self.gerar_snapshot:
                self.log_update.emit('SEÇÃO 4/5: GERAR SNAPSHOT')
                self.module_started.emit('report_snapshot')
                self.log_update.emit("Gerando snapshot...")
                gerar_report_snapshot()
                self.progress_update.emit('report_snapshot', 100)
                self.module_completed.emit('report_snapshot')
            else:
                self.progress_update.emit('report_snapshot', 0)
                self.log_update.emit("Geração de snapshot ignorada (opcional).")
            
            # SEÇÃO 5/5: ENCAMINHAR MENSAGEM
            self.log_update.emit('SEÇÃO 5/5: ENCAMINHAR MENSAGEM')
            
            # Comparar Excel
            self.log_update.emit("Comparando arquivos Excel...")
            novos = comparar_excel()
            
            # Enviar WhatsApp (opcional)
            if self.enviar_wpp:
                self.module_started.emit('whatsapp')
                self.log_update.emit("Enviando mensagem via WhatsApp...")
                
                fim = datetime.now()
                duracao = duracao_tempo(inicio, fim)
                link = "https://embrapii.sharepoint.com/:x:/r/sites/GEPES/Documentos%20Compartilhados/DWPII/srinfo/classificacao_projeto.xlsx?d=wb7a7a439310f4d52a37728b9f1833961&csf=1&web=1&e=qXpfgA"
                link_snapshot = "https://embrapii.sharepoint.com/:f:/r/sites/GEPES/Documentos%20Compartilhados/Reports?csf=1&web=1&e=aVdkyL"
                mensagem = (
                    f'*Pipeline SRInfo*\n'
                    f'Iniciado em: {inicio.strftime("%d/%m/%Y %H:%M:%S")}\n'
                    f'Finalizado em: {fim.strftime("%d/%m/%Y %H:%M:%S")}\n'
                    f'_Duração total: {duracao}_\n\n'
                    f'Novos projetos: {novos[0]}\n'
                    f'Novas empresas: {novos[1]}\n'
                    f'Projetos sem classificação: {novos[2]}\n\n'
                    f'Relatório Executivo (snapshot): {link_snapshot}\n\n'
                    f'Link para classificação dos projetos: {link}'
                )
                
                enviar_whatsapp(mensagem)
                self.progress_update.emit('whatsapp', 100)
                self.module_completed.emit('whatsapp')
            else:
                self.progress_update.emit('whatsapp', 0)
                self.log_update.emit("Envio de WhatsApp ignorado (opcional).")
            
            # Finalização
            fim = datetime.now()
            duracao = duracao_tempo(inicio, fim)
            self.log_update.emit(f'Fim: {fim.strftime("%d/%m/%Y %H:%M:%S")}')
            self.log_update.emit(f'Duração total: {duracao}')
            
            # Emitir estatísticas finais
            stats = {
                'inicio': inicio.strftime("%d/%m/%Y %H:%M:%S"),
                'fim': fim.strftime("%d/%m/%Y %H:%M:%S"),
                'duracao': duracao,
                'novos_projetos': novos[0],
                'novas_empresas': novos[1],
                'projetos_sem_classificacao': novos[2]
            }
            
            self.finished.emit(stats)
            
        except Exception as e:
            import traceback
            error_msg = f"Erro durante a execução do pipeline: {str(e)}\n{traceback.format_exc()}"
            self.log_update.emit(error_msg)
            self.error.emit(error_msg)
    
    def stop(self):
        self.running = False
        self.terminate()


class PipelineGUI(QMainWindow):
    """Interface gráfica principal para o Pipeline EMBRAPII SRInfo"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pipeline EMBRAPII SRInfo")
        self.setGeometry(100, 100, 1000, 800)
        
        # Componentes principais
        self.progress_bars = {}  # Barras de progresso para cada módulo
        self.module_labels = {}  # Labels para cada módulo
        self.log_display = QTextEdit()  # Área de exibição de logs
        self.start_button = QPushButton("Iniciar Pipeline")
        self.stop_button = QPushButton("Parar Pipeline")
        
        # Opções
        self.plano_metas_checkbox = QCheckBox("Processar Plano de Metas")
        self.snapshot_checkbox = QCheckBox("Gerar Snapshot")
        self.whatsapp_checkbox = QCheckBox("Enviar WhatsApp")
        
        # Estatísticas
        self.stats_display = QLabel()
        
        # Worker thread
        self.worker = None
        
        # Configuração do layout
        self.setup_ui()
        
        # Conexões de eventos
        self.start_button.clicked.connect(self.run_pipeline)
        self.stop_button.clicked.connect(self.stop_pipeline)
        self.stop_button.setEnabled(False)
    
    def setup_ui(self):
        """Configurar a interface do usuário"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("Pipeline EMBRAPII SRInfo")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Splitter para dividir a tela
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter, 1)
        
        # Área de progresso
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        
        # Grupo de opções
        options_group = QGroupBox("Opções")
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.plano_metas_checkbox)
        options_layout.addWidget(self.snapshot_checkbox)
        options_layout.addWidget(self.whatsapp_checkbox)
        options_group.setLayout(options_layout)
        progress_layout.addWidget(options_group)
        
        # Grupo de progresso
        progress_group = QGroupBox("Progresso dos Módulos")
        progress_group_layout = QVBoxLayout()
        
        # Scroll area para as barras de progresso
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Criar barras de progresso para cada módulo
        modules = [
            ('sharepoint', 'SharePoint - Buscar Arquivos'),
            ('info_empresas', 'Informações de Empresas'),
            ('empresas_contratantes', 'Empresas Contratantes'),
            ('info_unidades', 'Informações de Unidades'),
            ('equipe_ue', 'Equipe UE'),
            ('termos_cooperacao', 'Termos de Cooperação'),
            ('plano_acao', 'Plano de Ação'),
            ('plano_metas', 'Plano de Metas'),
            ('sebrae', 'Sebrae'),
            ('projetos_contratados', 'Projetos Contratados'),
            ('projetos_empresas', 'Projetos de Empresas'),
            ('projetos', 'Projetos'),
            ('contratos', 'Contratos'),
            ('estudantes', 'Estudantes'),
            ('pedidos_pi', 'Pedidos PI'),
            ('macroentregas', 'Macroentregas'),
            ('comunicacao', 'Comunicação'),
            ('eventos_srinfo', 'Eventos SRInfo'),
            ('prospeccao', 'Prospecção'),
            ('negociacoes', 'Negociações'),
            ('propostas_tecnicas', 'Propostas Técnicas'),
            ('planos_trabalho', 'Planos de Trabalho'),
            ('classificacao_projetos', 'Classificação de Projetos'),
            ('portfolio', 'Portfolio'),
            ('levar_arquivos_sharepoint', 'SharePoint - Enviar Arquivos'),
            ('report_snapshot', 'Relatório Snapshot'),
            ('whatsapp', 'Envio de WhatsApp')
        ]
        
        for module_id, module_name in modules:
            module_layout = QHBoxLayout()
            
            # Label do módulo
            label = QLabel(module_name)
            label.setMinimumWidth(200)
            self.module_labels[module_id] = label
            
            # Barra de progresso
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setTextVisible(True)
            self.progress_bars[module_id] = progress_bar
            
            module_layout.addWidget(label)
            module_layout.addWidget(progress_bar, 1)
            
            scroll_layout.addLayout(module_layout)
        
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        progress_group_layout.addWidget(scroll_area)
        progress_group.setLayout(progress_group_layout)
        progress_layout.addWidget(progress_group)
        
        # Botões de controle
        buttons_layout = QHBoxLayout()
        self.start_button.setMinimumHeight(40)
        self.stop_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        progress_layout.addLayout(buttons_layout)
        
        # Adicionar widget de progresso ao splitter
        splitter.addWidget(progress_widget)
        
        # Área de log
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        
        log_label = QLabel("Log de Execução")
        log_label.setAlignment(Qt.AlignCenter)
        log_font = QFont()
        log_font.setPointSize(12)
        log_font.setBold(True)
        log_label.setFont(log_font)
        log_layout.addWidget(log_label)
        
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display)
        
        # Estatísticas
        stats_group = QGroupBox("Estatísticas")
        stats_layout = QVBoxLayout()
        self.stats_display.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(self.stats_display)
        stats_group.setLayout(stats_layout)
        log_layout.addWidget(stats_group)
        
        # Adicionar widget de log ao splitter
        splitter.addWidget(log_widget)
        
        # Definir tamanhos iniciais do splitter
        splitter.setSizes([500, 300])
    
    def run_pipeline(self):
        """Iniciar a execução do pipeline em uma thread separada"""
        # Limpar interface
        self.clear_interface()
        
        # Desabilitar botão de início e habilitar botão de parada
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Desabilitar checkboxes
        self.plano_metas_checkbox.setEnabled(False)
        self.snapshot_checkbox.setEnabled(False)
        self.whatsapp_checkbox.setEnabled(False)
        
        # Criar e iniciar worker thread
        self.worker = PipelineWorker(
            plano_metas=self.plano_metas_checkbox.isChecked(),
            gerar_snapshot=self.snapshot_checkbox.isChecked(),
            enviar_wpp=self.whatsapp_checkbox.isChecked()
        )
        
        # Conectar sinais
        self.worker.progress_update.connect(self.update_progress)
        self.worker.log_update.connect(self.update_log)
        self.worker.module_started.connect(self.module_started)
        self.worker.module_completed.connect(self.module_completed)
        self.worker.finished.connect(self.pipeline_finished)
        self.worker.error.connect(self.pipeline_error)
        
        # Iniciar thread
        self.worker.start()
    
    def stop_pipeline(self):
        """Parar a execução do pipeline"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, 
                'Confirmar Parada', 
                'Tem certeza que deseja interromper o pipeline? Isso pode deixar dados em estado inconsistente.',
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker.stop()
                self.log_update("Pipeline interrompido pelo usuário.")
                
                # Habilitar botão de início e desabilitar botão de parada
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                
                # Habilitar checkboxes
                self.plano_metas_checkbox.setEnabled(True)
                self.snapshot_checkbox.setEnabled(True)
                self.whatsapp_checkbox.setEnabled(True)
    
    def clear_interface(self):
        """Limpar a interface para uma nova execução"""
        # Limpar log
        self.log_display.clear()
        
        # Limpar estatísticas
        self.stats_display.setText("")
        
        # Resetar barras de progresso
        for progress_bar in self.progress_bars.values():
            progress_bar.setValue(0)
            progress_bar.setStyleSheet("")
        
        # Resetar labels
        for label in self.module_labels.values():
            label.setStyleSheet("")
    
    def update_progress(self, module, value):
        """Atualizar a barra de progresso de um módulo"""
        if module in self.progress_bars:
            self.progress_bars[module].setValue(value)
    
    def update_log(self, message):
        """Adicionar mensagem ao log"""
        self.log_display.append(message)
        # Rolar para o final
        self.log_display.moveCursor(QTextCursor.End)
    
    def module_started(self, module):
        """Marcar um módulo como iniciado"""
        if module in self.module_labels:
            self.module_labels[module].setStyleSheet("color: blue; font-weight: bold;")
    
    def module_completed(self, module):
        """Marcar um módulo como concluído"""
        if module in self.module_labels:
            self.module_labels[module].setStyleSheet("color: green; font-weight: bold;")
    
    def pipeline_finished(self, stats):
        """Processar a conclusão do pipeline"""
        # Atualizar estatísticas
        stats_text = (
            f"<b>Início:</b> {stats['inicio']}<br>"
            f"<b>Fim:</b> {stats['fim']}<br>"
            f"<b>Duração:</b> {stats['duracao']}<br><br>"
            f"<b>Novos projetos:</b> {stats['novos_projetos']}<br>"
            f"<b>Novas empresas:</b> {stats['novas_empresas']}<br>"
            f"<b>Projetos sem classificação:</b> {stats['projetos_sem_classificacao']}"
        )
        self.stats_display.setText(stats_text)
        
        # Habilitar botão de início e desabilitar botão de parada
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Habilitar checkboxes
        self.plano_metas_checkbox.setEnabled(True)
        self.snapshot_checkbox.setEnabled(True)
        self.whatsapp_checkbox.setEnabled(True)
        
        # Mostrar mensagem de conclusão
        QMessageBox.information(
            self,
            "Pipeline Concluído",
            f"Pipeline concluído com sucesso!\n\nDuração: {stats['duracao']}\nNovos projetos: {stats['novos_projetos']}\nNovas empresas: {stats['novas_empresas']}"
        )
    
    def pipeline_error(self, error_msg):
        """Processar erro no pipeline"""
        # Habilitar botão de início e desabilitar botão de parada
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Habilitar checkboxes
        self.plano_metas_checkbox.setEnabled(True)
        self.snapshot_checkbox.setEnabled(True)
        self.whatsapp_checkbox.setEnabled(True)
        
        # Mostrar mensagem de erro
        QMessageBox.critical(
            self,
            "Erro no Pipeline",
            f"Ocorreu um erro durante a execução do pipeline:\n\n{error_msg}"
        )


# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipelineGUI()
    window.show()
    sys.exit(app.exec_())
