from hotel_app.extensions import mail, db
from flask import Blueprint, url_for, current_app
from flask_mail import Message

utils_bp = Blueprint('utils_bp', __name__)

# Sending confirmation mail
def send_confirmation_email(user_email, user):
    try:
        token = user.generate_confirmation_token()
        msg = Message('Confirm Your Account', sender='noreply@yourdomain.com', recipients=[user_email])
        msg.body = f'''Kindly confirm your account in the link below:
                    {url_for('user_bp.confirm_email', token=token, _external=True)}

                    If you did not make this request then simply ignore this email and no changes will be made.
                    '''
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send confirmation email: {e}")
 