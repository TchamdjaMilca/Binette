"""
Binette book !
"""
import logging
from flask import Flask, render_template, redirect
from compte import bp_compte
from mur import bp_mur
import bd
import os 
import dotenv



app = Flask(__name__)

if not os.getenv('BD_UTILISATEUR'):
    dotenv.load_dotenv('.env')

app.logger.setLevel(logging.DEBUG)
app.register_blueprint(bp_mur, url_prefix='/mur')
app.register_blueprint(bp_compte,url_prefix='/compte')

# Faire la commande suivante pour générer une chaîne aléatoire :
# python -c "import secrets; print(secrets.token_hex())
#la vie est dure.
app.secret_key =os.getenv('SECRET_SESSION') 


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
