from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES


class LDAPBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None and password is not None:
            if settings.LDAP_ENABLE:
                # Try connect to LDAP Server
                try:
                    server = Server(settings.LDAP_SERVER_URL, get_info=ALL)
                    with Connection(server, settings.LDAP_DN_STRING, settings.LDAP_PASSWORD,
                                    auto_bind=True) as connection:
                        if connection.search(settings.LDAP_CONTEXT, attributes=ALL_ATTRIBUTES,
                                             search_filter='(samaccountname=%s)' % (username,)):
                            results = connection.entries[0]
                            # Try login with username and password
                            if connection.rebind(results['distinguishedName'].values[0], password):
                                try:
                                    # Update Password
                                    user = User.objects.get(username__exact=username)
                                    user.set_password(password)
                                    user.save()
                                except User.DoesNotExist:
                                    # Create new User when not found
                                    user = User.objects.create_user(username, results['mail'].values[0], password,
                                                                    first_name=results['givenname'].values[0],
                                                                    last_name=results['sn'].values[0])
                                    # user.is_staff = True  # Add when you want join to the platform without permission
                                    user.save()
                                finally:
                                    return user
                except Exception as ex:
                    # Error in LDAP Server
                    return None
        return super(LDAPBackend, self).authenticate(request, username, password, **kwargs)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
