import stripe

from flask import Blueprint, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user, login_required

from models.pedido import Pedido


pagos = Blueprint('pagos', __name__)


@pagos.route('/pagar/<int:pedido_id>', methods=['POST'])
@login_required
def crear_checkout_session(pedido_id):
    stripe_secret_key = current_app.config.get("STRIPE_SECRET_KEY")
    base_url = current_app.config.get("BASE_URL").rstrip("/")

    if not stripe_secret_key:
        flash('No se ha configurado correctamente la clave de Stripe.', 'danger')
        return redirect(url_for('main.mis_pedidos'))

    stripe.api_key = stripe_secret_key

    pedido = Pedido.get_by_id(pedido_id)

    if not pedido:
        flash('El pedido no existe.', 'danger')
        return redirect(url_for('main.mis_pedidos'))

    if pedido.user_id != current_user.id:
        flash('No tienes permisos para pagar este pedido.', 'danger')
        return redirect(url_for('main.mis_pedidos'))

    if pedido.estado_pago == 'pagado':
        flash('Este pedido ya está pagado.', 'warning')
        return redirect(url_for('main.mis_pedidos'))

    if pedido.estado_pedido != 'aceptado':
        flash('Solo puedes pagar pedidos que hayan sido aceptados.', 'warning')
        return redirect(url_for('main.mis_pedidos'))

    if not pedido.precio_total or float(pedido.precio_total) <= 0:
        flash('El pedido no tiene un importe válido.', 'danger')
        return redirect(url_for('main.mis_pedidos'))

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            customer_email=pedido.email_cliente,
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Reserva Valstrax Rail #{pedido.id}',
                            'description': f'{pedido.origen} → {pedido.destino} | {pedido.espacios_solicitados} m²'
                        },
                        'unit_amount': int(float(pedido.precio_total) * 100),
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                'pedido_id': str(pedido.id),
                'codigo_seguimiento': str(pedido.codigo_seguimiento)
            },
            success_url=f'{base_url}/pago/exito?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{base_url}/pago/cancelado'
        )

        Pedido.update_stripe_session(pedido.id, session.id)

        print("Checkout session creada")
        print("Pedido ID:", pedido.id)
        print("Session ID:", session.id)

        return redirect(session.url, code=303)

    except stripe.error.StripeError as e:
        print("Error de Stripe:", e)
        flash('No se ha podido iniciar el pago con Stripe.', 'danger')
        return redirect(url_for('main.mis_pedidos'))

    except Exception as e:
        print("Error inesperado al crear el pago:", e)
        flash('Ha ocurrido un error al preparar el pago.', 'danger')
        return redirect(url_for('main.mis_pedidos'))


@pagos.route('/pago/exito')
@login_required
def pago_exito():
    flash('Pago realizado correctamente. Tu pedido se actualizará en unos segundos.', 'success')
    return redirect(url_for('main.mis_pedidos'))


@pagos.route('/pago/cancelado')
@login_required
def pago_cancelado():
    flash('El pago ha sido cancelado. Puedes intentarlo de nuevo cuando quieras.', 'warning')
    return redirect(url_for('main.mis_pedidos'))


@pagos.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    stripe_secret_key = current_app.config.get("STRIPE_SECRET_KEY")
    endpoint_secret = current_app.config.get("STRIPE_WEBHOOK_SECRET")

    if not stripe_secret_key:
        return jsonify({'error': 'Stripe no configurado'}), 500

    stripe.api_key = stripe_secret_key

    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )

    except ValueError as e:
        print("Webhook error - Payload inválido:", e)
        return jsonify({'error': 'Payload inválido'}), 400

    except stripe.error.SignatureVerificationError as e:
        print("Webhook error - Firma inválida:", e)
        return jsonify({'error': 'Firma inválida'}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        stripe_session_id = session['id']
        payment_intent_id = session['payment_intent']

        metadata = session['metadata']
        pedido_id = metadata['pedido_id'] if 'pedido_id' in metadata else None

        print("WEBHOOK checkout.session.completed")
        print("Pedido ID:", pedido_id)
        print("Stripe session:", stripe_session_id)
        print("Payment intent:", payment_intent_id)

        if pedido_id:
            Pedido.marcar_pagado(
                pedido_id,
                stripe_session_id,
                payment_intent_id
            )

    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        stripe_session_id = session['id']

        Pedido.marcar_cancelado_por_session(stripe_session_id)

    return jsonify({'received': True}), 200