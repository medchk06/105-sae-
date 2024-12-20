import re
from datetime import datetime

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
        evenement['DESCRIPTION'] = re.search(r'DESCRIPTION:(.*)', bloc)
        
        # Remplacer les valeurs manquantes par "vide"
        evenement = {k: (v.group(1) if v else "vide") for k, v in evenement.items()}
        evenements.append(evenement)
    
    return evenements

def filtrer_evenements(evenements, ressource, groupe_tp):
    """Filtre les événements pour la ressource et le groupe TP spécifiés."""
    resultats = []
    
    for evenement in evenements:
        summary = evenement['SUMMARY']
        if ressource in summary and groupe_tp in summary:
            # Extraire la date
            date = evenement['DTSTART'][:8]
            date_formattee = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")
            
            # Calculer la durée
            dtstart = datetime.strptime(evenement['DTSTART'], "%Y%m%dT%H%M%S")
            dtend = datetime.strptime(evenement['DTEND'], "%Y%m%dT%H%M%S")
            duree = (dtend - dtstart).seconds // 60  # Durée en minutes
            
            # Identifier le type de séance (CM, TD, TP)
            type_seance = "TP" if "TP" in summary else ("TD" if "TD" in summary else "CM")
            
            # Ajouter au tableau des résultats
            resultats.append([date_formattee, duree, type_seance])
    
    return resultats

def main():
    # Chemin du fichier ICS
    fichier_ics = r"C:/Users/userlocal/Downloads/ADE_RT1_Septembre2023_Decembre2023.ics"
    
    # Paramètres de filtre
    ressource = "R1.07"
    groupe_tp = "TP Groupe B1"  # Remplacez par votre groupe
    
    # Lire et traiter le fichier
    contenu_ics = lire_fichier_ics(fichier_ics)
    evenements = extraire_evenements(contenu_ics)
    
    # Filtrer les événements
    seances_filtrees = filtrer_evenements(evenements, ressource, groupe_tp)
    
    # Afficher le tableau filtré
    print("Tableau des séances filtrées :")
    for seance in seances_filtrees:
        print(seance)

if __name__ == "__main__":
    main()
