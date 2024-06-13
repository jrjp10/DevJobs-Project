# For creating simple-jwt authenication token

from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken

# Generate Token Manually
def get_token_for_users(user):
    try:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    except Exception as e:
        # Log the error for investigation
        print(f"Token generation failed for user {user.email}: {e}")
        # Return None or an empty dictionary indicating failure
        return None
    

# For creating token for emailverification
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        """
        Generate a hash value for the given user and timestamp.
        """
        return (text_type(user.uuid) + text_type(timestamp) + text_type(user.is_active))

generate_token = TokenGenerator()