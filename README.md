# Documentação do Sistema de Automação de E-mail para WhatsApp

## Visão Geral
Este código implementa um sistema automatizado que realiza as seguintes funções:
1. Monitora uma caixa de e-mail específica
2. Busca e-mails do Looker Studio
3. Extrai imagens desses e-mails
4. Envia as imagens automaticamente via WhatsApp (para um grupo específico)

## Requisitos do Sistema
- Python 3.x
- Bibliotecas necessárias:
  - imaplib
  - email
  - python-dotenv
  - pywhatkit
  - logging
  - pywin32

## Estrutura do Projeto
```
projeto/
│
├── logs/                  # Diretório para arquivos de log
├── Relatorios_diarios/   # Diretório para salvar as imagens
├── .env                  # Arquivo de configuração com variáveis de ambiente
└── main.py              # Código principal
```

## Configuração
### Variáveis de Ambiente (.env)
```
IMAP_SERVER=seu_servidor_imap (Gmail ou qualquer outro)
EMAIL_ADDRESS=seu_email
EMAIL_PASSWORD=sua_senha
WHATSAPP_NUMBER=numero_whatsapp (ID do grupo do Whats)
```

## Principais Funções

### 1. setup_logging()
- Configura o sistema de logs
- Cria arquivos de log com data/hora
- Define formato e nível de logging

### 2. load_env_variables()
- Carrega variáveis do arquivo .env
- Retorna dicionário com configurações

### 3. connect_to_imap()
- Estabelece conexão com servidor IMAP
- Realiza autenticação do e-mail

### 4. fetch_and_save_images()
- Busca e-mails do Looker Studio
- Extrai e salva imagens
- Organiza por data em pastas

### 5. send_whatsapp_image()
- Envia imagens via WhatsApp
- Utiliza threading para controle de tempo
- Adiciona legenda padrão

## Fluxo de Execução
1. Inicia configuração de logs
2. Carrega variáveis de ambiente
3. Conecta ao servidor IMAP
4. Busca e salva imagens
5. Envia imagens via WhatsApp
6. Finaliza execução

## Tratamento de Erros
- Logging de erros em arquivo
- Verificação de variáveis de ambiente
- Timeout para envios de WhatsApp
- Tratamento de exceções em operações críticas

## Uso
```bash
# Execução normal
python main.py

# Modo configuração
python main.py --config
```

## Observações Importantes
1. Necessário WhatsApp Web conectado
2. Intervalo de 60s entre envios
3. Timeout de 900s para envios
4. Imagens são salvas com nome único
5. Logs detalhados de todas operações

## Manutenção
Para atualizar a versão, siga os passos:
1. Use Git Bash no terminal
2. Execute `git add --all`
3. Verifique com `git status`
4. Commit com mensagem: `git commit -m 'mensagem'`
5. Push das alterações: `git push`
6. Confirme com `git status`
