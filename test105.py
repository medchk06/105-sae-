import re

def tcp_analyse(chemin_fichier):
    # Patterns regex simplifiés pour les informations essentielles
    patterns = {
        'Horodatage': r'(\d{2}:\d{2}:\d{2}\.\d{6})',
        'Adresse_Source': r'IP (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
        'Adresse_Destination': r'> (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
        'Port_Source': r'\.(\d+) >',
        'Port_Destination': r'> .+?\.(\d+):',
        'Flags': r'\[(\w+)\]',
        'Length': r'length (\d+)'
    }
    
    try:
        with open(chemin_fichier, 'r') as file:
            for line in file:
                # Ignorer les lignes vides
                if not line.strip():
                    continue
                    
                result = {}
                for key, pattern in patterns.items():
                    match = re.search(pattern, line)
                    if match:
                        result[key] = match.group(1)
                
                # N'afficher que si des données ont été trouvées
                if result:
                    print("\nAnalyse de paquet:")
                    for key, value in result.items():
                        if value:
                            print(f"{key}: {value}")
                            
    except FileNotFoundError:
        print(f"Le fichier '{chemin_fichier}' n'existe pas.")
    except Exception as e:
        print(f"Erreur: {e}")

# Utilisation
chemin_fichier = 'DumpFile.txt'
tcp_analyse(chemin_fichier)