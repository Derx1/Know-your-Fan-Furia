![image]([https://github.com/user-attachments/assets/a01fc4d8-5787-49a8-9490-2d9e575fe6bf](https://www.google.com/imgres?q=furia%20logo&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fpt%2Ff%2Ff9%2FFuria_Esports_logo.png&imgrefurl=https%3A%2F%2Fpt.wikipedia.org%2Fwiki%2FFicheiro%3AFuria_Esports_logo.png&docid=AyInFgcVH5A9sM&tbnid=XrwWxAOJi8PBMM&vet=12ahUKEwjZ2I6j8omNAxVBJ7kGHZR6NDcQM3oECB0QAA..i&w=321&h=312&hcb=2&ved=2ahUKEwjZ2I6j8omNAxVBJ7kGHZR6NDcQM3oECB0QAA))# Know Your Fan - FURIA

![FURIA Logo](static/images/furia-logo.png)

## Sobre o Projeto

O **Know Your Fan** é uma plataforma inovadora desenvolvida para a FURIA E-Sports com o objetivo de conhecer melhor os fãs da organização e oferecer experiências exclusivas baseadas nos seus perfis e interesses. Esta aplicação permite coletar e analisar dados de perfis de fãs, incluindo suas preferências em jogos, times favoritos, documentos de identidade verificados e conexões com redes sociais e plataformas de e-sports.

## Funcionalidades Principais

- **Cadastro e Login**: Sistema seguro de autenticação de usuários
- **Perfil Completo**: Coleta de dados pessoais e interesses em e-sports
- **Verificação de Identidade**: Upload e verificação de documentos usando IA
- **Conexão de Redes Sociais**: Vinculação e análise de perfis sociais
- **Integração com Plataformas de E-sports**: Validação de perfis em plataformas como Steam, Riot Games, etc.
- **Dashboard Personalizado**: Visualização de status de verificação e benefícios disponíveis

## Equipes FURIA Integradas

A plataforma inclui informações e links para todas as equipes da FURIA:

- [Counter-Strike 2](https://liquipedia.net/counterstrike/FURIA)
- [Valorant](https://liquipedia.net/valorant/FURIA)
- [Rocket League](https://liquipedia.net/rocketleague/FURIA)
- [Rainbow Six](https://liquipedia.net/rainbowsix/FURIA)
- [League of Legends](https://liquipedia.net/leagueoflegends/FURIA)
- [PUBG](https://liquipedia.net/pubg/FURIA)
- [Kings League](https://kingsleague.pro/pt/times/50-furia-fc)

## Tecnologias Utilizadas

- **Backend**: Python 3.10+, Flask 2.3+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL (produção)
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF
- **ORM**: SQLAlchemy
- **Simulação IA**: Serviços de análise de documentos e perfis sociais

## Requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Outras dependências listadas em `requirements.txt`

## Instalação e Configuração

### Instalação Local

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/know-your-fan.git
   cd know-your-fan
   ```

2. Crie e ative um ambiente virtual Python:
   ```
   python -m venv venv
   
   # Ativação no Windows
   venv\Scripts\activate
   
   # Ativação no macOS/Linux
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente (opcional):
   ```
   # No Windows (PowerShell)
   $env:SECRET_KEY="sua-chave-secreta"
   $env:DATABASE_URI="sqlite:///knowyourfan.db"
   $env:FLASK_APP="app.py"
   $env:FLASK_DEBUG="1"
   
   # No macOS/Linux
   export SECRET_KEY=sua-chave-secreta
   export DATABASE_URI=sqlite:///knowyourfan.db
   export FLASK_APP=app.py
   export FLASK_DEBUG=1
   ```

5. Inicialize o banco de dados:
   ```
   flask shell
   >>> from app import app, db
   >>> with app.app_context():
   >>>     db.create_all()
   >>> exit()
   ```
   
   Ou simplesmente execute a aplicação, que inicializará o banco de dados automaticamente:
   ```
   python app.py
   ```

6. Execute a aplicação:
   ```
   flask run
   # ou
   python app.py
   ```

7. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

### Usando Docker (Opcional)

1. Construa a imagem Docker:
   ```
   docker build -t know-your-fan .
   ```

2. Execute o contêiner:
   ```
   docker run -p 5000:5000 --name know-your-fan-app know-your-fan
   ```

3. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

### Modo de Demonstração

O sistema possui um modo de demonstração que cria um usuário pré-configurado:

1. Acesse a rota de demonstração:
   ```
   http://localhost:5000/demo
   ```

2. Você será automaticamente logado com a conta de demonstração:
   - Email: demo@furia.com
   - Senha: demo123

## Uso da Aplicação

### Para Usuários

1. **Cadastro e Login**:
   - Crie uma conta com seu email e senha
   - Faça login para acessar todas as funcionalidades

2. **Perfil Completo**:
   - Complete seu perfil com informações pessoais
   - Adicione seus interesses em e-sports, jogos favoritos e histórico como fã

3. **Verificação de Documentos**:
   - Faça upload de documentos de identidade para verificação
   - Aguarde a validação automática (simulada pela IA)

4. **Conexão de Redes Sociais**:
   - Vincule suas contas de redes sociais
   - Permita a análise de seu perfil para recomendações personalizadas

5. **Integração com E-sports**:
   - Adicione seus perfis de plataformas de jogos
   - Conecte contas como Steam, Faceit, etc.

### Para Administradores

A interface administrativa inclui:

1. **Gestão de Usuários**:
   - Visualização de todos os perfis de fãs
   - Aprovação manual de verificações pendentes

2. **Análise de Dados**:
   - Visualização de estatísticas e tendências
   - Exportação de relatórios

3. **Gerenciamento de Conteúdo**:
   - Atualização de informações sobre times e eventos
   - Criação de ofertas exclusivas para fãs verificados

## Estrutura do Projeto

```
know-your-fan/
│
├── app.py                 # Ponto de entrada principal da aplicação
├── models.py              # Modelos de banco de dados
├── forms.py               # Definições de formulários
├── ai_services.py         # Serviços simulados de IA
├── requirements.txt       # Dependências do projeto
├── Procfile               # Configuração para deploy no Heroku
├── run_app.bat            # Script para execução rápida no Windows
├── setup_task.ps1         # Script PowerShell para configuração
│
├── static/                # Arquivos estáticos
│   ├── site.css           # Estilos CSS personalizados
│   ├── images/            # Imagens do site incluindo o logo da FURIA
│   └── uploads/           # Uploads de usuários acessíveis via web
│       ├── documents/     # Documentos verificados
│       └── profiles/      # Fotos de perfil
│
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── home.html          # Página inicial
│   ├── about.html         # Página sobre
│   ├── register.html      # Página de registro
│   ├── login.html         # Página de login
│   ├── dashboard.html     # Dashboard do usuário
│   ├── profile.html       # Perfil do usuário
│   ├── documents.html     # Verificação de documentos
│   ├── social.html        # Conexão de redes sociais
│   └── esports.html       # Validação de perfis de e-sports
│
├── uploads/               # Diretório para uploads de arquivos
│   ├── documents/         # Documentos enviados pelos usuários
│   └── profiles/          # Fotos de perfil
│
└── instance/              # Diretório para dados específicos da instância
    └── knowyourfan.db     # Banco de dados SQLite
```

## Serviços de IA (Simulação)

O projeto inclui simulações de serviços de IA para demonstrar as funcionalidades:

- **DocumentAIService**: Simula verificação de documentos de identidade
  - Verifica se um documento é válido e autêntico
  - Extrai informações como nome e número do documento
  - Compara com dados fornecidos pelo usuário

- **SocialMediaAnalyzer**: Simula análise de perfis em redes sociais
  - Extrai interesses relacionados a e-sports
  - Identifica times seguidos e nível de engajamento
  - Calcula score de relevância para e-sports

- **EsportsProfileValidator**: Simula validação de perfis em plataformas de e-sports
  - Verifica a autenticidade dos perfis informados
  - Extrai estatísticas de jogo e nível de habilidade
  - Determina relevância do perfil para o ecossistema de e-sports

## Personalização

### Alteração de Cores e Tema

O tema utiliza variáveis CSS que podem ser facilmente modificadas no arquivo `static/site.css`:

```css
:root {
    --primary-color: #1e88e5;     /* Cor principal */
    --secondary-color: #ff9800;   /* Cor secundária */
    --dark-color: #212121;        /* Cor escura */
    --light-color: #f5f5f5;       /* Cor clara */
    --furia-color: #000000;       /* Cor principal da FURIA */
    --furia-accent: #ffffff;      /* Cor secundária da FURIA */
    --furia-red: #ff0000;         /* Cor de destaque da FURIA */
}
```

### Adição de Novas Páginas

Para adicionar uma nova página:

1. Crie um novo template HTML na pasta `templates/`
2. Adicione a rota correspondente no arquivo `app.py`
3. Adicione um link para a nova página na navegação (`base.html`)

## Implantação em Produção

### Heroku

O projeto já inclui um `Procfile` para deployment no Heroku:

1. Crie uma aplicação no Heroku:
   ```
   heroku create sua-aplicacao
   ```

2. Configure as variáveis de ambiente:
   ```
   heroku config:set SECRET_KEY=sua-chave-secreta
   heroku config:set DATABASE_URI=postgres://...
   ```

3. Faça o deploy:
   ```
   git push heroku main
   ```

### Servidor Linux (VPS)

1. Clone o repositório no servidor
2. Configure um servidor WSGI (Gunicorn, uWSGI)
3. Configure o Nginx como proxy reverso
4. Configure o supervisor ou systemd para manter a aplicação rodando

Exemplo de configuração Nginx:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Convenções de Código

- Siga o padrão PEP 8 para código Python
- Utilize docstrings para documentar funções e classes
- Mantenha o código organizado e modular

## Próximos Passos

- Implementar autenticação OAuth para redes sociais reais
- Integrar APIs reais de plataformas de e-sports
- Adicionar sistema de notificações para eventos
- Desenvolver painel administrativo para a equipe FURIA
- Implementar sistema de recompensas baseado em engajamento
- Integrar sistema de análise de sentimentos para feedback dos fãs
- Expandir suporte para mais jogos e plataformas

## Solução de Problemas

### Problemas Comuns

1. **Erro ao inicializar o banco de dados**
   - Verifique se você tem permissões de escrita no diretório `instance`
   - Tente excluir o arquivo de banco de dados existente e reiniciar a aplicação

2. **Erro ao fazer upload de arquivos**
   - Verifique se os diretórios `uploads` e `static/uploads` existem e têm permissões corretas
   - Verifique o tamanho máximo de upload configurado

3. **Problemas de login/autenticação**
   - Limpe os cookies do navegador
   - Verifique se `SECRET_KEY` está configurado corretamente

## Recursos Adicionais

- [Site Oficial FURIA](https://www.furia.gg/)
- [Documentação do Flask](https://flask.palletsprojects.com/)
- [Documentação do Bootstrap](https://getbootstrap.com/docs/)
- [Tutoriais de Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Tutoriais de Flask Login](https://flask-login.readthedocs.io/)

## Licença

Este projeto é propriedade da FURIA E-Sports e seu uso é restrito aos propósitos da organização.

---

Desenvolvido para FURIA E-Sports © 2025
