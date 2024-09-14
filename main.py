import subprocess
import webbrowser
import os


def debug():
    """
    :return: Traitement flake8
    """
    try:
        subprocess.run(["flake8", "--format=html", "--htmldir=verify_flake8_rapport"])

        try:
            chemin = os.getcwd()
            fichier_html = f"{chemin}/verify_flake8_rapport/index.html"
            webbrowser.open(fichier_html)

        except ValueError as er:
            print("Erreur lors de l'ouverture du fichier :", er)

    except subprocess.CalledProcessError as e:
        print(f"Erreur : {e}")


if __name__ == '__main__':
    debug()
