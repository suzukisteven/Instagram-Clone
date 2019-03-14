import datetime
import braintree
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
from instagram_web import gateway, TRANSACTION_SUCCESS_STATUSES, generate_client_token, transact, find_transaction
# This is __init__.py from the root level


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

@donations_blueprint.route('/new', methods=['GET'])
def new():
    client_token = generate_client_token()
    return render_template('donations/new.html', client_token=client_token)

@donations_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
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

@donations_blueprint.route('/checkouts', methods=['POST'])
def create():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('donations.show',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('donations.new'))

