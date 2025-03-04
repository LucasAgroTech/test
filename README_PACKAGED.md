# Pipeline EMBRAPII SRInfo - Versão Empacotada

## Sobre

Esta é a versão empacotada do Pipeline EMBRAPII SRInfo, que inclui uma interface gráfica para facilitar o acompanhamento e execução do processo de extração, transformação e carga de dados do SRInfo da Embrapii para o DWPII.

## Requisitos

- Sistema operacional Windows
- Microsoft Edge instalado (necessário para o WebDriver)
- Acesso à internet
- Credenciais válidas para o SRInfo e SharePoint da Embrapii

## Instalação

1. Extraia o conteúdo do arquivo ZIP para uma pasta de sua preferência
2. Certifique-se de que o arquivo `.env` está presente na pasta raiz do aplicativo
3. Execute o arquivo `Pipeline EMBRAPII SRInfo.exe`

## Configuração

O arquivo `.env` deve conter as seguintes variáveis de ambiente:

```env
ROOT=<caminho para a pasta raiz do projeto>
SRINFO_USERNAME=<nome de usuário de acesso ao SRInfo>
PASSWORD=<senha de acesso ao SRInfo>
PASTA_DOWNLOAD=<caminho para a pasta downloads>

sharepoint_email=<email de acesso ao SharePoint>
sharepoint_password=<senha de acesso ao SharePoint>
sharepoint_url_site=<URL do site SharePoint>
sharepoint_site_name=<nome do site SharePoint>
sharepoint_doc_library=<biblioteca de documentos>
```

## Utilização

### Interface Gráfica

A interface gráfica do Pipeline EMBRAPII SRInfo é dividida em três seções principais:

1. **Opções**: Permite selecionar quais etapas opcionais do pipeline serão executadas:

   - **Processar Plano de Metas**: Inclui o processamento do plano de metas
   - **Gerar Snapshot**: Gera um relatório snapshot ao final do processo
   - **Enviar WhatsApp**: Envia uma mensagem via WhatsApp com o resumo da operação

2. **Progresso dos Módulos**: Exibe o progresso de cada módulo do pipeline com barras de progresso individuais. Os módulos são coloridos de acordo com seu estado:

   - **Azul**: Módulo em execução
   - **Verde**: Módulo concluído com sucesso
   - **Cinza**: Módulo ainda não iniciado ou ignorado (opcional)

3. **Log de Execução**: Exibe mensagens detalhadas sobre o andamento do processo, permitindo acompanhar cada etapa em tempo real.

4. **Estatísticas**: Após a conclusão do pipeline, exibe estatísticas sobre a execução, incluindo:
   - Horário de início e fim
   - Duração total
   - Número de novos projetos
   - Número de novas empresas
   - Número de projetos sem classificação

### Botões de Controle

- **Iniciar Pipeline**: Inicia a execução do pipeline com as opções selecionadas
- **Parar Pipeline**: Interrompe a execução do pipeline (use com cautela, pois pode deixar dados em estado inconsistente)

## Sequência de Execução

O pipeline segue a mesma sequência lógica da versão original:

1. **Verificação e criação da estrutura de diretórios**
2. **Busca de arquivos no SharePoint**
3. **Coleta de dados do SRInfo** (várias etapas)
4. **Processamento dos dados coletados**
5. **Carregamento dos dados no DWPII**
6. **Geração de snapshot** (opcional)
7. **Envio de mensagem via WhatsApp** (opcional)

## Solução de Problemas

### O aplicativo não inicia

- Verifique se o arquivo `.env` está presente e configurado corretamente
- Certifique-se de que todas as pastas referenciadas no arquivo `.env` existem
- Verifique se o Microsoft Edge está instalado no sistema

### Erro durante a execução

- Verifique as mensagens de erro no log de execução
- Certifique-se de que as credenciais do SRInfo e SharePoint estão corretas
- Verifique se há conexão com a internet

### Problemas com o WebDriver

- Certifique-se de que o Microsoft Edge está atualizado
- Verifique se o WebDriver Manager consegue baixar a versão correta do driver

## Suporte

Para suporte ou dúvidas sobre o aplicativo, entre em contato com a equipe de desenvolvimento.
