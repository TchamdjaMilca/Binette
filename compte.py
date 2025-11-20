"""Pour gérer l'authentification"""
from flask import Blueprint, render_template, request, redirect, session, current_app as app
import bd
from utilitaires import hacher_mdp

bp_compte = Blueprint('compte', __name__)

@bp_compte.route("/authentifier", methods=['GET','POST'])
def authentifier():
    """effectuer l'authentification"""
    erreur = False
    courriel = request.form.get("courriel", default="")
    mdp = ""

    if (request.method== 'POST'):
        app.logger.info("Debut d'auth")

        mdp = hacher_mdp(request.form.get("mdp"))
        with bd.creer_connexion() as conn:
            utilisateur = bd.authentifier(conn, courriel, mdp)

        erreur = (not utilisateur)

        if not erreur:
            session["utilisateur"] = utilisateur["id_utilisateur"], utilisateur["nom"]
            print(session["utilisateur"])
            return redirect('/', code=303)
    
    return render_template('compte/authentifier.jinja', courriel=courriel, mdp=mdp, erreur=erreur)
        

@bp_compte.route('/deconnecter', methods=['GET'])
def deconnecter():
    """deconnecter"""

    if "utilisateur" in session:
        app.logger.info("Deconnexion de session")

    session.clear()
    return redirect('/', code=303)