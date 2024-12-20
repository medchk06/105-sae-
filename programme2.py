import re

def lire_fichier_ics(nom_fichier):
    """Lit le contenu d'un fichier ICS et le retourne sous forme de texte."""
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    return contenu

def extraire_evenements(ics_contenu):
    """Extrait tous les événements d'un fichier ICS."""
    evenements = []
    # Repérer les blocs de chaque événement entre BEGIN:VEVENT et END:VEVENT
    blocs_evenements = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", ics_contenu, re.S)
    
    for bloc in blocs_evenements:
        evenement = {}
        # Extraire les champs nécessaires ou insérer "vide" si non trouvé
        evenement['SUMMARY'] = re.search(r'SUMMARY:(.*)', bloc)
        evenement['DTSTART'] = re.search(r'DTSTART:(.*)', bloc)
        evenement['DTEND'] = re.search(r'DTEND:(.*)', bloc)
        evenement['LOCATION'] = re.search(r'LOCATION:(.*)', bloc)
        evenement['DESCRIPTION'] = re.search(r'DESCRIPTION:(.*)', bloc)
        
        # Remplacer les valeurs manquantes par "vide"
        evenement = {k: (v.group(1) if v else "vide") for k, v in evenement.items()}
        evenements.append(evenement)
    
    return evenements

def convertir_en_csv(evenement):
    """Convertit un événement en une ligne pseudo-CSV."""
    # Conversion des dates/horaires
    dtstart = (
        evenement['DTSTART'][:8] + " " + evenement['DTSTART'][9:11] + ":" + evenement['DTSTART'][11:13]
        if evenement['DTSTART'] != "vide" else "vide"
    )
    dtend = (
        evenement['DTEND'][:8] + " " + evenement['DTEND'][9:11] + ":" + evenement['DTEND'][11:13]
        if evenement['DTEND'] != "vide" else "vide"
    )
    
    # Construction de la ligne CSV
    csv_ligne = f'"{evenement["SUMMARY"]}","{dtstart}","{dtend}","{evenement["LOCATION"]}","{evenement["DESCRIPTION"]}"'
    return csv_ligne

def main():
    # Chemin du fichier ICS
    fichier_ics = r"C:/Users/userlocal/Downloads/ADE_RT1_Septembre2023_Decembre2023.ics"
    
    # Lire et traiter le fichier
    contenu_ics = lire_fichier_ics(fichier_ics)
    evenements = extraire_evenements(contenu_ics)
    
    # Convertir les événements en pseudo-CSV
    tableau_csv = [convertir_en_csv(evenement) for evenement in evenements]
    
    # Afficher le tableau CSV
    print("Tableau CSV :")
    for ligne in tableau_csv:
        print(ligne)

if __name__ == "__main__":
    main()
