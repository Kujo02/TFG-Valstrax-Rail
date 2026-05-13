from flask_wtf import FlaskForm
from wtforms.validators import Email,EqualTo,Length,DataRequired,NumberRange
from wtforms.fields import EmailField,StringField,PasswordField,SubmitField,SelectField,IntegerField,DateTimeLocalField

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


class VagonForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='El nombre del vagón es obligatorio.'),
            Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres.')
        ]
    )

    filas = IntegerField('Filas',validators=[DataRequired(message='El número de filas es obligatorio.'),
            NumberRange(min=1, max=10, message='Las filas deben estar entre 1 y 10.')
        ]
    )

    columnas = IntegerField('Columnas',validators=[DataRequired(message='El número de columnas es obligatorio.'),
            NumberRange(min=1, max=30, message='Las columnas deben estar entre 1 y 30.')
        ]
    )

    estado_vagon = SelectField('Estado',choices=[('activo', 'Activo'),('inactivo', 'Inactivo')],
            validators=[
            DataRequired(message='El estado del vagón es obligatorio.')
        ]
    )

    submit = SubmitField('Guardar')



class ViajeForm(FlaskForm):
    tren_id = SelectField('Tren',coerce=int,validators=[DataRequired(message='Debes seleccionar un tren.')
        ]
    )

    origen = StringField('Origen',validators=[DataRequired(message='El origen es obligatorio.'),
            Length(min=2, max=100, message='El origen debe tener entre 2 y 100 caracteres.')
        ]
    )

    destino = StringField('Destino',validators=[DataRequired(message='El destino es obligatorio.'),
            Length(min=2, max=100, message='El destino debe tener entre 2 y 100 caracteres.')
        ]
    )

    fecha_salida = DateTimeLocalField('Fecha de salida',format='%Y-%m-%dT%H:%M',
        validators=[DataRequired(message='La fecha de salida es obligatoria.')
        ]
    )

    fecha_llegada = DateTimeLocalField('Fecha de llegada',format='%Y-%m-%dT%H:%M')

    estado_viaje = SelectField('Estado',
        choices=[
            ('programado', 'Programado'),
            ('en_transito', 'En tránsito'),
            ('finalizado', 'Finalizado'),
            ('cancelado', 'Cancelado')
        ],
        validators=[
            DataRequired(message='El estado del viaje es obligatorio.')
        ]
    )

    submit = SubmitField('Guardar')