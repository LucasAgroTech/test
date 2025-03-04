# Guia de Teste do Pipeline EMBRAPII SRInfo Empacotado

Este guia fornece instruções detalhadas sobre como testar o aplicativo Pipeline EMBRAPII SRInfo após o empacotamento, garantindo que todas as funcionalidades estejam operando corretamente.

## 1. Preparação para Teste

### 1.1 Verificação do Ambiente

Antes de iniciar os testes, certifique-se de que:

- O Microsoft Edge está instalado e atualizado
- Há conexão com a internet
- As credenciais do SRInfo e SharePoint estão válidas
- O arquivo `.env` está configurado corretamente

### 1.2 Preparação do Diretório de Teste

1. Crie uma pasta separada para testes (ex: `C:\Teste_Pipeline`)
2. Copie todo o conteúdo da pasta `dist/pipeline_embrapii_srinfo` para esta pasta
3. Verifique se o arquivo `.env` está presente e contém as configurações corretas
4. Certifique-se de que o arquivo `Pipeline EMBRAPII SRInfo.exe` está presente

## 2. Testes Básicos

### 2.1 Teste de Inicialização

1. Execute o arquivo `Pipeline EMBRAPII SRInfo.exe`
2. Verifique se a interface gráfica é carregada corretamente
3. Confirme se todos os elementos da interface estão visíveis:
   - Checkboxes de opções
   - Barras de progresso para cada módulo
   - Área de log
   - Botões de controle

### 2.2 Teste de Configuração

1. Marque e desmarque as opções (Processar Plano de Metas, Gerar Snapshot, Enviar WhatsApp)
2. Verifique se as opções permanecem no estado selecionado

## 3. Testes Funcionais

### 3.1 Teste de Execução Parcial

Para testar rapidamente se o pipeline está funcionando sem executar todo o processo:

1. Modifique temporariamente o arquivo `.env` para apontar para diretórios de teste
2. Inicie o aplicativo
3. Clique em "Iniciar Pipeline"
4. Observe se o processo inicia corretamente:
   - A estrutura de diretórios é criada
   - O log exibe mensagens de progresso
   - As barras de progresso são atualizadas
5. Após verificar que o início do processo está funcionando, clique em "Parar Pipeline"
6. Confirme a interrupção quando solicitado
7. Verifique se o processo foi interrompido corretamente

### 3.2 Teste de Execução Completa (Opcional)

Se possível e desejável, realize um teste completo:

1. Configure o arquivo `.env` com valores reais
2. Inicie o aplicativo
3. Selecione as opções desejadas
4. Clique em "Iniciar Pipeline"
5. Acompanhe o processo completo, verificando:
   - Progresso de cada módulo
   - Mensagens no log
   - Atualização das barras de progresso
   - Mudança de cor dos módulos (azul durante execução, verde após conclusão)
6. Ao final, verifique as estatísticas exibidas

## 4. Testes de Integração

### 4.1 Teste de Integração com SharePoint

1. Verifique se o aplicativo consegue acessar o SharePoint:
   - Observe as mensagens de log relacionadas ao SharePoint
   - Confirme se arquivos são baixados/enviados corretamente

### 4.2 Teste de Integração com WebDriver

1. Verifique se o WebDriver é inicializado corretamente:
   - Observe as mensagens de log relacionadas ao WebDriver
   - Confirme se o navegador Edge é aberto durante o processo

### 4.3 Teste de Integração com WhatsApp (se aplicável)

1. Marque a opção "Enviar WhatsApp"
2. Execute o pipeline (ou parte dele)
3. Verifique se a mensagem é enviada corretamente via WhatsApp

## 5. Testes de Recuperação de Erros

### 5.1 Teste de Credenciais Inválidas

1. Modifique temporariamente o arquivo `.env` com credenciais inválidas
2. Execute o aplicativo e inicie o pipeline
3. Verifique se o erro é tratado adequadamente:
   - Mensagem de erro é exibida no log
   - Interface não trava
   - É possível reiniciar o processo após corrigir as credenciais

### 5.2 Teste de Interrupção

1. Inicie o pipeline
2. Interrompa o processo clicando em "Parar Pipeline"
3. Verifique se:
   - O processo é interrompido corretamente
   - A interface volta ao estado inicial
   - É possível iniciar um novo processo

## 6. Verificação Final

Após concluir os testes, verifique:

1. Se todos os arquivos necessários foram criados nos diretórios apropriados
2. Se os logs foram registrados corretamente
3. Se não há erros ou exceções não tratadas
4. Se o aplicativo pode ser fechado e reaberto sem problemas

## 7. Solução de Problemas Comuns

### 7.1 Erro de WebDriver

Se o WebDriver não inicializar corretamente:

- Verifique se o Microsoft Edge está instalado e atualizado
- Verifique se há conexão com a internet para baixar o driver
- Tente executar o aplicativo como administrador

### 7.2 Erro de Acesso ao SharePoint

Se houver problemas de acesso ao SharePoint:

- Verifique as credenciais no arquivo `.env`
- Confirme se as URLs do SharePoint estão corretas
- Verifique se há conexão com a internet

### 7.3 Erro de Permissão de Arquivos

Se houver problemas de acesso a arquivos:

- Verifique se o aplicativo tem permissão para acessar os diretórios configurados
- Execute o aplicativo como administrador
- Verifique se os caminhos no arquivo `.env` estão corretos

## 8. Documentação de Testes

Recomenda-se documentar os resultados dos testes, incluindo:

- Data e hora do teste
- Versão do aplicativo testado
- Problemas encontrados
- Soluções aplicadas

Esta documentação será útil para futuras atualizações e solução de problemas.
