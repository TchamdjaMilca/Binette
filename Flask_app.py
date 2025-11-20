"""
Binette book !
"""
import logging
from flask import Flask, render_template, redirect
from compte import bp_compte
from mur import bp_mur
import bd


app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
app.register_blueprint(bp_mur, url_prefix='/mur')
app.register_blueprint(bp_compte,url_prefix='/compte')

# Faire la commande suivante pour générer une chaîne aléatoire :
# python -c "import secrets; print(secrets.token_hex())"
app.secret_key = "Cette chaîne servira pour l'encryption de la session. \
                  Elle doit être générée aléatoirement"


@app.route('/')
def index():
    """Affiche l'accueil"""
    app.logger.info("Affichage des utilisateurs")
    with bd.creer_connexion() as conn:
        utilisateurs = bd.get_utilisateurs(conn)
    return render_template('index.jinja', utilisateurs=utilisateurs)

@app.errorhandler(401)
def non_autorise(e):
    app.logger.exception(e)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
