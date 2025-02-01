from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Incluye el ID del usuario, su estado de verificación, el timestamp y la ultima actualizacion del usuario en el hash
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.verified) + six.text_type(user.updated_at)
        )

generate_token = TokenGenerator()