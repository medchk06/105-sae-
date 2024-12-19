import re

def lire_fichier_ics(nom_fichier):
    """Lit le contenu d'un fichier ICS et le retourne sous forme de texte."""
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    return contenu

def extraire_evenement(ics_contenu):
    """Extrait les données d'un événement ICS et les retourne sous forme de dictionnaire."""
    evenement = {}
    # Utilisation de regex pour extraire les champs d'intérêt
    evenement['SUMMARY'] = re.search(r'SUMMARY:(.*)', ics_contenu).group(1)
    evenement['DTSTART'] = re.search(r'DTSTART:(.*)', ics_contenu).group(1)
    evenement['DTEND'] = re.search(r'DTEND:(.*)', ics_contenu).group(1)
    evenement['LOCATION'] = re.search(r'LOCATION:(.*)', ics_contenu).group(1)
    evenement['DESCRIPTION'] = re.search(r'DESCRIPTION:(.*)', ics_contenu).group(1)
    return evenement

def convertir_en_csv(evenement):
    """Convertit les données d'un événement en une ligne pseudo-CSV."""
    # Conversion des dates/horaires
    dtstart = evenement['DTSTART'][:8] + " " + evenement['DTSTART'][9:11] + ":" + evenement['DTSTART'][11:13]
    dtend = evenement['DTEND'][:8] + " " + evenement['DTEND'][9:11] + ":" + evenement['DTEND'][11:13]
    
    # Construction de la chaîne CSV
    csv_ligne = f'"{evenement["SUMMARY"]}","{dtstart}","{dtend}","{evenement["LOCATION"]}","{evenement["DESCRIPTION"]}"'
    return csv_ligne

def main():
    # Chemin du fichier ICS
    fichier_ics = "C:/Users/userlocal/Downloads/evenementSAE_15(1).ics"
    
    # Lire et traiter le fichier
    contenu_ics = lire_fichier_ics(fichier_ics)
    evenement = extraire_evenement(contenu_ics)
    resultat_csv = convertir_en_csv(evenement)
    
    # Afficher le résultat
    print("Pseudo-CSV :")
    print(resultat_csv)

if __name__ == "__main__":
    main()
