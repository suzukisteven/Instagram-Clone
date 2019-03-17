import datetime
import braintree
import sendgrid
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.money import Money, User, Image
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app, deliver_email
from instagram_web import gateway, TRANSACTION_SUCCESS_STATUSES, generate_client_token, transact, find_transaction
# This ^ is __init__.py from the root level

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

@donations_blueprint.route('/<image_id>/new', methods=['GET'])
def new(image_id):
    image = Image.get(id=image_id)
    client_token = generate_client_token()
    return render_template('donations/new.html', image=image, client_token=client_token)

@donations_blueprint.route('/donations/<transaction_id>', methods=['GET'])
def show(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('donations/show.html', transaction=transaction, result=result)

@donations_blueprint.route('<image_id>/checkouts', methods=['POST'])
def create(image_id):
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        # Create a new donation record: amount, user_id=current_user.id and image_id of the image that was donated to.
        user_id = current_user.id
        amount = request.form.get('amount')
        Money.create(amount=amount, user_id=current_user.id, image_id=image_id)
        deliver_email()
        return redirect(url_for('donations.show', image_id=image_id, transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('donations.new', image_id=image_id))