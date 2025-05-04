import os
import secrets
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from models import db, User, Profile, Document, SocialAccount, EsportsProfile
from forms import RegistrationForm, LoginForm, ProfileForm, DocumentUploadForm, SocialAccountForm, EsportsProfileForm
from ai_services import DocumentAIService, SocialMediaAnalyzer, EsportsProfileValidator

# Cria e configura a aplicação
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'desenvolvimento-temporario')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///knowyourfan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Garantir que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)

# Criar também uma pasta de uploads dentro de static para imagens acessíveis pela web
os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
os.makedirs(os.path.join('static', 'uploads', 'profiles'), exist_ok=True)
os.makedirs(os.path.join('static', 'uploads', 'documents'), exist_ok=True)

# Inicializar SQLAlchemy com o app
db.init_app(app)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Cria as tabelas do banco de dados se elas não existirem
with app.app_context():
    db.create_all()
    print("Banco de dados inicializado com sucesso!")

# Funções auxiliares
def save_picture(form_picture, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, picture_fn)
    form_picture.save(picture_path)
    
    # Salvar também na pasta static para acesso web
    static_path = os.path.join('static', 'uploads', folder, picture_fn)
    form_picture.seek(0)  # Voltar ao início do arquivo
    try:
        with open(static_path, 'wb') as f:
            f.write(form_picture.read())
    except Exception as e:
        print(f"Erro ao salvar imagem em static: {e}")
    
    return picture_fn

# Rotas
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Verificar se o e-mail já existe no banco de dados
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            flash('Este e-mail já está cadastrado. Por favor, use outro e-mail ou faça login.', 'danger')
            return render_template('register.html', title='Cadastro', form=form)
            
        # Verificar se o nome de usuário já existe
        existing_user_name = User.query.filter_by(username=form.username.data).first()
        if existing_user_name:
            flash('Este nome de usuário já está em uso. Por favor, escolha outro nome de usuário.', 'danger')
            return render_template('register.html', title='Cadastro', form=form)
            
        # Se nem o e-mail nem o nome de usuário existem, criar o novo usuário
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastro', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login efetuado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login falhou. Por favor verifique email e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    # Pré-preencher o formulário com dados existentes
    if request.method == 'GET':
        if current_user.name:
            form.name.data = current_user.name
        if current_user.cpf:
            form.cpf.data = current_user.cpf
        if current_user.birth_date:
            form.birth_date.data = current_user.birth_date
        if current_user.address:
            form.address.data = current_user.address
        if current_user.profile:
            if current_user.profile.interests:
                form.interests.data = current_user.profile.interests
            if current_user.profile.fan_story:
                form.fan_story.data = current_user.profile.fan_story
            if current_user.profile.favorite_games:
                favorite_games = current_user.profile.favorite_games.split(',')
                form.favorite_games.data = [game.strip() for game in favorite_games if game.strip()]
            if current_user.profile.other_games:
                form.other_games.data = current_user.profile.other_games
            if current_user.profile.favorite_teams:
                favorite_teams = current_user.profile.favorite_teams.split(',')
                form.favorite_teams.data = [team.strip() for team in favorite_teams if team.strip()]
            if current_user.profile.other_teams:
                form.other_teams.data = current_user.profile.other_teams
            if current_user.profile.events_attended:
                events_attended = current_user.profile.events_attended.split(',')
                form.events_attended.data = [event.strip() for event in events_attended if event.strip()]
            if current_user.profile.other_events:
                form.other_events.data = current_user.profile.other_events
            if current_user.profile.purchases:
                form.purchases.data = current_user.profile.purchases
    
    if form.validate_on_submit():
        # Atualizar dados do usuário
        current_user.name = form.name.data
        current_user.cpf = form.cpf.data
        current_user.birth_date = form.birth_date.data
        current_user.address = form.address.data
        
        # Verificar se o perfil já existe ou criar um novo
        if not current_user.profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
        else:
            profile = current_user.profile
        
        # Atualizar dados do perfil
        profile.interests = form.interests.data
        profile.fan_story = form.fan_story.data
        profile.favorite_games = ','.join(form.favorite_games.data) if form.favorite_games.data else ''
        profile.other_games = form.other_games.data
        profile.favorite_teams = ','.join(form.favorite_teams.data) if form.favorite_teams.data else ''
        profile.other_teams = form.other_teams.data
        profile.events_attended = ','.join(form.events_attended.data) if form.events_attended.data else ''
        profile.other_events = form.other_events.data
        profile.purchases = form.purchases.data
        
        # Salvar foto de perfil, se enviada
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data, 'profiles')
            profile.profile_picture = picture_file
        
        db.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('profile.html', title='Perfil', form=form)

@app.route("/documents", methods=['GET', 'POST'])
@login_required
def documents():
    form = DocumentUploadForm()
    if form.validate_on_submit():
        # Salvar o documento
        document_file = save_picture(form.document.data, 'documents')
        document = Document(
            user_id=current_user.id,
            filename=document_file,
            doc_type=form.doc_type.data
        )
        db.session.add(document)
        db.session.commit()
        
        # Verificar documento com IA
        document_path = os.path.join(app.config['UPLOAD_FOLDER'], 'documents', document_file)
        verification_result = DocumentAIService.verify_identity_document(
            document_path, 
            expected_name=current_user.name, 
            expected_cpf=current_user.cpf
        )
        
        # Atualizar status de verificação do documento
        if verification_result['is_valid']:
            document.verified = True
            document.verification_date = datetime.utcnow()
            db.session.commit()
            flash('Documento enviado e verificado com sucesso!', 'success')
        else:
            flash('Documento enviado, mas não foi possível verificar automaticamente. Nossa equipe fará uma verificação manual.', 'warning')
        
        return redirect(url_for('documents'))
    
    # Listar documentos do usuário
    user_documents = Document.query.filter_by(user_id=current_user.id).all()
    
    return render_template('documents.html', title='Documentos', form=form, documents=user_documents)

@app.route("/social", methods=['GET', 'POST'])
@login_required
def social():
    form = SocialAccountForm()
    if form.validate_on_submit():
        # Em um cenário real, seria feita a autenticação OAuth
        # Aqui vamos apenas simular a vinculação da conta
        
        # Verificar se a conta já existe
        existing_account = SocialAccount.query.filter_by(
            user_id=current_user.id,
            platform=form.platform.data,
            username=form.username.data
        ).first()
        
        if not existing_account:
            # Criar nova conta social
            account = SocialAccount(
                user_id=current_user.id,
                platform=form.platform.data,
                username=form.username.data,
                access_token="dummy_token",
                last_sync=datetime.utcnow()
            )
            db.session.add(account)
            db.session.commit()
            
            # Analisar perfil social com IA
            analysis = SocialMediaAnalyzer.analyze_social_profile(
                form.platform.data,
                form.username.data
            )
            
            if analysis['success']:
                flash(f'Conta de {form.platform.data} conectada com sucesso!', 'success')
            else:
                flash('Conta conectada, mas não foi possível analisar o perfil.', 'warning')
        else:
            flash('Esta conta já está vinculada ao seu perfil.', 'info')
        
        return redirect(url_for('social'))
    
    # Listar contas sociais do usuário
    social_accounts = SocialAccount.query.filter_by(user_id=current_user.id).all()
    
    return render_template('social.html', title='Redes Sociais', form=form, accounts=social_accounts)

@app.route("/esports", methods=['GET', 'POST'])
@login_required
def esports():
    form = EsportsProfileForm()
    if form.validate_on_submit():
        # Validar URL do perfil
        if EsportsProfileValidator.validate_profile_url(form.platform.data, form.profile_url.data):
            # Analisar perfil com IA
            analysis = EsportsProfileValidator.analyze_esports_profile(
                form.platform.data,
                form.profile_url.data
            )
            
            # Criar novo perfil de esports
            profile = EsportsProfile(
                user_id=current_user.id,
                platform=form.platform.data,
                profile_url=form.profile_url.data,
                username=form.username.data or analysis.get('username', ''),
                verified=analysis['success'],
                relevance_score=analysis.get('relevance_score', 0.0),
                verified_date=datetime.utcnow() if analysis['success'] else None
            )
            db.session.add(profile)
            db.session.commit()
            
            if analysis['success'] and analysis.get('is_relevant_to_esports', False):
                flash('Perfil de e-sports adicionado e validado com sucesso!', 'success')
            else:
                flash('Perfil adicionado, mas com baixa relevância para e-sports.', 'warning')
        else:
            flash('A URL do perfil parece inválida para a plataforma selecionada.', 'danger')
        
        return redirect(url_for('esports'))
    
    # Listar perfis de e-sports do usuário
    esports_profiles = EsportsProfile.query.filter_by(user_id=current_user.id).all()
    
    return render_template('esports.html', title='Perfis de E-Sports', form=form, profiles=esports_profiles)

@app.route("/api/verify_document", methods=['POST'])
@login_required
def api_verify_document():
    if 'document' not in request.files:
        return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'})
    
    file = request.files['document']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'})
    
    document_file = save_picture(file, 'documents')
    document_path = os.path.join(app.config['UPLOAD_FOLDER'], 'documents', document_file)
    
    # Verificar documento com IA
    verification_result = DocumentAIService.verify_identity_document(
        document_path, 
        expected_name=current_user.name, 
        expected_cpf=current_user.cpf
    )
    
    return jsonify({
        'success': True,
        'verification': verification_result
    })

@app.route("/api/analyze_social", methods=['POST'])
@login_required
def api_analyze_social():
    data = request.json
    if not data or 'platform' not in data or 'username' not in data:
        return jsonify({'success': False, 'error': 'Dados incompletos'})
    
    # Analisar perfil social com IA
    analysis = SocialMediaAnalyzer.analyze_social_profile(
        data['platform'],
        data['username']
    )
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route("/api/validate_esports_profile", methods=['POST'])
@login_required
def api_validate_esports_profile():
    data = request.json
    if not data or 'platform' not in data or 'url' not in data:
        return jsonify({'success': False, 'error': 'Dados incompletos'})
    
    # Validar URL
    is_valid = EsportsProfileValidator.validate_profile_url(data['platform'], data['url'])
    if not is_valid:
        return jsonify({'success': False, 'error': 'URL inválida para a plataforma'})
    
    # Analisar perfil
    analysis = EsportsProfileValidator.analyze_esports_profile(
        data['platform'],
        data['url']
    )
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route("/demo")
def demo():
    """Rota especial para modo demonstração, cria um usuário de teste se não existir"""
    demo_email = "demo@furia.com"
    demo_user = User.query.filter_by(email=demo_email).first()
    
    if not demo_user:
        # Criar usuário demo
        demo_user = User(
            username="demo_user",
            email=demo_email
        )
        demo_user.set_password("demo123")
        db.session.add(demo_user)
        db.session.commit()
        
        # Criar alguns dados de exemplo
        profile = Profile(
            user_id=demo_user.id,
            interests="Counter-Strike 2, Valorant, e-sports competitivo",
            fan_story="Sou fã da FURIA desde sua fundação em 2017, acompanhando principalmente o time de CS.",
            favorite_games="cs2,valorant",
            favorite_teams="furia_cs2,furia_valorant",
            events_attended="major_copenhagen_2024"
        )
        db.session.add(profile)
        
        # Adicionar uma conta social de exemplo
        social = SocialAccount(
            user_id=demo_user.id,
            platform="twitter",
            username="demo_furia_fan",
            last_sync=datetime.utcnow()
        )
        db.session.add(social)
        
        db.session.commit()
        flash("Conta de demonstração criada com sucesso!", "success")
    
    # Fazer login com a conta demo
    login_user(demo_user)
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
