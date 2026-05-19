from flask_mail import Message
from extensions import mail


def enviar_correo_seguimiento(pedido):
    asunto = 'Tu reserva en Valstrax Rail'

    cuerpo_texto = f"""
Hola {pedido.nombre_cliente},

Tu reserva se ha registrado correctamente en Valstrax Rail y queda pendiente de revisión.

Código de seguimiento: {pedido.codigo_seguimiento}

Datos del pedido:
Ruta: {pedido.origen} -> {pedido.destino}
Tren: {pedido.tren_nombre} ({pedido.tren_codigo})
Fecha de salida: {pedido.fecha_salida}
Fecha de llegada: {pedido.fecha_llegada or 'Sin definir'}
Espacio solicitado: {pedido.espacios_solicitados} m²
Estado actual: {pedido.estado_pedido}

Puedes consultar el estado de tu pedido desde la sección Seguimiento introduciendo tu email y el código anterior.

Gracias por confiar en Valstrax Rail.
"""

    cuerpo_html = f"""
    <div style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 24px; color: #1f2937;">
        <div style="max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 14px; overflow: hidden; border: 1px solid #e5e7eb;">

            <div style="background-color: #1e3a8a; padding: 24px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 28px;">
                    Valstrax Rail
                </h1>
                <p style="margin: 8px 0 0 0; color: #bfdbfe;">
                    Confirmación de reserva
                </p>
            </div>

            <div style="padding: 28px;">
                <p style="font-size: 16px; margin-top: 0;">
                    Hola <strong>{pedido.nombre_cliente}</strong>,
                </p>

                <p style="font-size: 15px; line-height: 1.6;">
                    Tu reserva se ha registrado correctamente y queda pendiente de revisión por parte de administración.
                </p>

                <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 18px; border-radius: 10px; margin: 24px 0;">
                    <p style="margin: 0; color: #1e3a8a; font-weight: bold; font-size: 14px; text-transform: uppercase;">
                        Código de seguimiento
                    </p>
                    <p style="font-size: 28px; font-weight: bold; margin: 8px 0 0 0; color: #111827; letter-spacing: 1px;">
                        {pedido.codigo_seguimiento}
                    </p>
                </div>

                <h2 style="font-size: 20px; color: #1e3a8a; margin-bottom: 14px;">
                    Datos del pedido
                </h2>

                <table style="width: 100%; border-collapse: collapse; font-size: 15px;">
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #6b7280;">
                            Ruta
                        </td>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: bold;">
                            {pedido.origen} → {pedido.destino}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #6b7280;">
                            Tren
                        </td>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: bold;">
                            {pedido.tren_nombre} ({pedido.tren_codigo})
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #6b7280;">
                            Fecha de salida
                        </td>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: bold;">
                            {pedido.fecha_salida}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #6b7280;">
                            Fecha de llegada
                        </td>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: bold;">
                            {pedido.fecha_llegada or 'Sin definir'}
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #6b7280;">
                            Espacio solicitado
                        </td>
                        <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: bold;">
                            {pedido.espacios_solicitados} m²
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 10px; color: #6b7280;">
                            Estado actual
                        </td>
                        <td style="padding: 10px; font-weight: bold;">
                            {pedido.estado_pedido}
                        </td>
                    </tr>
                </table>

                <p style="font-size: 15px; line-height: 1.6; margin-top: 24px;">
                    Puedes consultar el estado de tu pedido desde la sección <strong>Seguimiento</strong>
                    introduciendo tu email y el código anterior.
                </p>

                <p style="font-size: 15px; line-height: 1.6;">
                    Gracias por confiar en Valstrax Rail.
                </p>
            </div>

            <div style="background-color: #f9fafb; padding: 16px; text-align: center; color: #6b7280; font-size: 13px;">
                Este correo se ha generado automáticamente. No respondas a este mensaje.
            </div>

        </div>
    </div>
    """

    mensaje = Message(
        subject=asunto,
        recipients=[pedido.email_cliente],
        body=cuerpo_texto,
        html=cuerpo_html
    )

    mail.send(mensaje)