from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, URL
import re

class RegistrationForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    birth_date = DateField('Data de Nascimento', validators=[DataRequired()])
    address = StringField('Endereço', validators=[DataRequired()])
    interests = TextAreaField('Interesses em e-sports')
    fan_story = TextAreaField('Conte-nos sua história como fã')
    favorite_games = SelectMultipleField('Jogos favoritos', choices=[
        ('cs2', 'Counter-Strike 2'),
        ('valorant', 'Valorant'),
        ('rocketleague', 'Rocket League'),
        ('r6', 'Rainbow Six'),
        ('lol', 'League of Legends'),
        ('pubg', 'PUBG'),
        ('dota2', 'Dota 2'),
        ('fifa', 'EA Sports FC'),
        ('fortnite', 'Fortnite'),
        ('apex', 'Apex Legends'),
        ('overwatch', 'Overwatch'),
        ('hearthstone', 'Hearthstone'),
        ('starcraft2', 'StarCraft 2'),
        ('other', 'Outro (Especificar)'),
    ])
    other_games = TextAreaField('Outros jogos (se necessário)')
    favorite_teams = SelectMultipleField('Times favoritos', choices=[
        ('furia_cs2', 'FURIA CS2'),
        ('furia_valorant', 'FURIA Valorant'),
        ('furia_rl', 'FURIA Rocket League'),
        ('furia_r6', 'FURIA R6'),
        ('furia_lol', 'FURIA LoL'),
        ('furia_pubg', 'FURIA PUBG'),
        ('furia_fc', 'FURIA FC (Kings League)')
    ])
    other_teams = TextAreaField('Outros times (se necessário)')
    events_attended = SelectMultipleField('Eventos que participou', choices=[
        ('major_austin_2025', 'Major CS2 Austin 2025'),
        ('major_copenhagen_2024', 'Major CS2 Copenhagen 2024'),
        ('valorant_champions_2025', 'Valorant Champions Tour 2025'),
        ('vct_americas_2025', 'VCT Americas 2025'),
        ('cblol_2025', 'CBLOL 2025'),
        ('six_invitational_2025', 'Six Invitational 2025'),
        ('kings_world_cup_2025', 'Kings World Cup 2025'),
        ('blast_premier_2025', 'BLAST Premier 2025'),
        ('rlcs_2025', 'RLCS World Championship 2025'),
        ('esl_pro_league_s19', 'ESL Pro League Season 19'),
        ('other', 'Outro (Especificar)'),
    ])
    other_events = TextAreaField('Outros eventos (se necessário)')
    purchases = TextAreaField('Compras relacionadas a e-sports no último ano')
    profile_picture = FileField('Foto de perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens são permitidas!')
    ])
    submit = SubmitField('Atualizar Perfil')

    def validate_cpf(self, cpf):
        # Remover caracteres não numéricos
        cpf_digits = re.sub(r'[^0-9]', '', cpf.data)
        
        if len(cpf_digits) != 11:
            raise ValidationError('CPF deve conter 11 dígitos')
        
        # Verificar se todos os dígitos são iguais
        if cpf_digits == cpf_digits[0] * 11:
            raise ValidationError('CPF inválido')
        
        # Validação do primeiro dígito verificador
        sum_of_products = sum(int(a) * b for a, b in zip(cpf_digits[:-2], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10) % 11
        if expected_digit == 10:
            expected_digit = 0
        if int(cpf_digits[-2]) != expected_digit:
            raise ValidationError('CPF inválido')
        
        # Validação do segundo dígito verificador
        sum_of_products = sum(int(a) * b for a, b in zip(cpf_digits[:-1], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10) % 11
        if expected_digit == 10:
            expected_digit = 0
        if int(cpf_digits[-1]) != expected_digit:
            raise ValidationError('CPF inválido')

class DocumentUploadForm(FlaskForm):
    document = FileField('Documento', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Apenas imagens e PDFs são permitidos!')
    ])
    doc_type = SelectField('Tipo de Documento', choices=[
        ('id', 'Documento de Identidade'),
        ('cpf', 'CPF'),
        ('address', 'Comprovante de Residência'),
        ('selfie', 'Selfie com Documento')
    ])
    submit = SubmitField('Enviar Documento')

class SocialAccountForm(FlaskForm):
    platform = SelectField('Plataforma', choices=[
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('twitch', 'Twitch')
    ])
    username = StringField('Nome de usuário', validators=[DataRequired()])
    submit = SubmitField('Vincular Conta')

class EsportsProfileForm(FlaskForm):
    platform = SelectField('Plataforma', choices=[
        ('steam', 'Steam'),
        ('battlenet', 'Battle.net'),
        ('riot', 'Riot Games'),
        ('faceit', 'FACEIT'),
        ('hltv', 'HLTV'),
        ('other', 'Outro')
    ])
    profile_url = StringField('URL do Perfil', validators=[DataRequired(), URL()])
    username = StringField('Nome de usuário na plataforma')
    submit = SubmitField('Adicionar Perfil')