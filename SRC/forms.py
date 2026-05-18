from flask_wtf import FlaskForm
from wtforms.validators import Email,EqualTo,Length,DataRequired,NumberRange,Optional
from wtforms.fields import EmailField,StringField,PasswordField,SubmitField,SelectField,IntegerField,DateTimeLocalField,TextAreaField


#FORMULARIOS USUARIOS



# FROMULARIO REGISTRO

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirmar')

# FORMULARIO LOGIN

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirmar')




# FORMULARIOS ADMIN


# FORMULARIO TRENES

class TrenForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='El nombre del tren es obligatorio.'),
            Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres.')
        ]
    )

    codigo = StringField('Código',validators=[DataRequired(message='El código del tren es obligatorio.'),
            Length(min=2, max=50, message='El código debe tener entre 2 y 50 caracteres.')
        ]
    )

    estado_tren = SelectField('Estado',choices=[('activo', 'Activo'),('inactivo', 'Inactivo')
        ],
        validators=[
            DataRequired(message='El estado del tren es obligatorio.')
        ]
    )

    estacion_actual_id = SelectField('Estación actual',coerce=int,
        validators=[
            DataRequired(message='Debes seleccionar una estación actual.')
        ]
    )

    submit = SubmitField('Guardar')

# FORMULARIO VAGONES


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


# FORMULARIO VIAJES

class ViajeForm(FlaskForm):
    tren_id = SelectField('Tren',coerce=int,validators=[DataRequired(message='Debes seleccionar un tren.')])

    origen_id = SelectField('Estación de origen',coerce=int,validators=[
            DataRequired(message='Debes seleccionar una estación de origen.')
        ]
    )

    destino_id = SelectField('Estación de destino',coerce=int,validators=[
            DataRequired(message='Debes seleccionar una estación de destino.')
        ]
    )

    fecha_salida = DateTimeLocalField('Fecha de salida',format='%Y-%m-%dT%H:%M',
        validators=[
            DataRequired(message='La fecha de salida es obligatoria.')
        ]
    )

    fecha_llegada = DateTimeLocalField('Fecha de llegada',format='%Y-%m-%dT%H:%M',validators=[Optional()]
    )

    estado_viaje = SelectField(
        'Estado',
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

# FORMULARIO PEDIDOS

class PedidoForm(FlaskForm):
    nombre_cliente = StringField('Nombre',validators=[DataRequired(message='El nombre es obligatorio.'),
            Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres.')
        ]
    )

    email_cliente = StringField('Email',validators=[DataRequired(message='El email es obligatorio.'),
            Email(message='Introduce un email válido.'),
            Length(max=150, message='El email no puede superar los 150 caracteres.')
        ]
    )

    descripcion = TextAreaField('Descripción de la carga',validators=[DataRequired(message='La descripción es obligatoria.'),
            Length(min=5, max=500, message='La descripción debe tener entre 5 y 500 caracteres.')
        ]
    )

    espacios_solicitados = IntegerField('Espacios solicitados (m²)',validators=[
            DataRequired(message='Debes indicar los m² solicitados.'),
            NumberRange(min=1, max=500, message='Los espacios solicitados deben estar entre 1 y 500 m².')
        ]
    )

    submit = SubmitField('Reservar')


# FORMULARIO ESTACIONES

class EstacionForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='El nombre de la estación es obligatorio.'),
            Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres.')
        ]
    )

    ciudad = StringField('Ciudad',validators=[DataRequired(message='La ciudad es obligatoria.'),
            Length(min=2, max=100, message='La ciudad debe tener entre 2 y 100 caracteres.')
        ]
    )

    codigo = StringField('Código',validators=[DataRequired(message='El código de la estación es obligatorio.'),
            Length(min=2, max=20, message='El código debe tener entre 2 y 20 caracteres.')
        ]
    )

    estado_estacion = SelectField('Estado',choices=[('activa', 'Activa'),('inactiva', 'Inactiva')
        ],
        validators=[
            DataRequired(message='El estado de la estación es obligatorio.')
        ]
    )

    submit = SubmitField('Guardar')