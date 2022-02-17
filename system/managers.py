from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES


class LDAPBackend(ModelBackend):
    """Autenticacion por LDAP"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None and password is not None:
            # Usar LDAP si esta habilitado
            if settings.LDAP_ENABLE:
                # Intentar conectar al servidor de LDAP
                try:
                    server = Server(settings.LDAP_SERVER_URL, get_info=ALL)
                    with Connection(server, settings.LDAP_DN_STRING, settings.LDAP_PASSWORD,
                                    auto_bind=True) as connection:
                        # Buscar el usuario
                        if connection.search(settings.LDAP_CONTEXT, attributes=ALL_ATTRIBUTES,
                                             search_filter='(samaccountname=%s)' % (username,)):
                            results = connection.entries[0]
                            # Intentar logearse con los datos proporcionados
                            if connection.rebind(results['distinguishedName'].values[0], password):
                                try:
                                    # Si el usuario existe actualizo la contrasena por si contienen una antigua
                                    user = User.objects.get(username__exact=username)
                                    user.set_password(password)
                                    user.save()
                                except User.DoesNotExist:
                                    # Creo un usuario si no existe por si no hay conexion con LDAP autenticar con DJANGO
                                    user = User.objects.create_user(username, results['mail'].values[0], password,
                                                                    first_name=results['givenName'].values[0],
                                                                    last_name=results['sn'].values[0])
                                    # Agregar acceso al sistema si no es profesor
                                    user.is_staff = results['title'].values[0] != 'Estudiante'
                                    user.save()
                                finally:
                                    return user
                except Exception as ex:
                    # Error in LDAP Server
                    return None
        return super(LDAPBackend, self).authenticate(request, username, password, **kwargs)

    def get_user(self, user_id):
        """Devolver usuario segun el ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
