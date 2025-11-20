"""
Fonctions utilitaires
"""

from flask import abort, session
import hashlib
import bd


def get_utilisateur_or_die(conn, identifiant, code=404):
    """Retourne le profile d'un utilisateur existant ou faire un abort(code)"""
    profile = bd.get_utilisateur(conn, identifiant)
    if profile is None:
        abort(code)
    return profile

# ANCIEN get utilisateur authentifié
# def get_utilisateur_authenifie_or_die(code=401):
#     """authentifier"""
#     if "utilisateur" in session:
#         return session["utilisateur"]
#     abort(code)

def get_utilisateur_authentifie_or_die():
    """Retourne l'utilisateur authentifié ou faire un abort(code)"""
    if "utilisateur" not in session :
        abort(401)

    return session["utilisateur"][0]    # pour accéder à l'identifiant


def est_un_ami(identifiant_a_chercher, amis):
    """Indique si un identifiant est dans la liste des amis"""
    for ami in amis:
        if ami["id_utilisateur"] == identifiant_a_chercher:
            return True
    return False

def hacher_mdp(mdp_clair):
    """hacher mdp"""
    return hashlib.sha512(mdp_clair.encode('utf-8')).hexdigest()
