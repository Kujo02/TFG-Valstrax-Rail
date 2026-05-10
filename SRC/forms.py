from flask_wtf import FlaskForm
from wtforms.validators import Email,EqualTo,Length,DataRequired
from wtforms.fields import EmailField,StringField,PasswordField,SubmitField

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirmar')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirmar')


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class TrenForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='El nombre es obligatorio.'),
            Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')
        ]
    )

    codigo = StringField('Código',validators=[ DataRequired(message='El código es obligatorio.'),
            Length(min=3, max=50, message='El código debe tener entre 3 y 50 caracteres.')
        ]
    )

    estado_tren = SelectField('Estado',choices=[('activo', 'Activo'),('inactivo', 'Inactivo')],
        validators=[DataRequired(message='El estado es obligatorio.')]
    )

    submit = SubmitField('Guardar')