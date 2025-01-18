import csv
import matplotlib.pyplot as plt
import os
import tempfile
import shutil

# Fonction pour analyser le fichier et extraire les informations pertinentes
def analyser_fichier(filepath):
    with open(filepath, "r") as fichier:
        ipsr, ipde, longueur, flag, seq, heure = [], [], [], [], [], []
        flagcounterP, flagcounterS, flagcounter, framecounter = 0, 0, 0, 0
        requestcounter, replycounter, seqcounter, ackcounter, wincounter = 0, 0, 0, 0, 0

        for ligne in fichier:
            split = ligne.split(" ")
            if "IP" in ligne:
                framecounter += 1
                if "[P.]" in ligne:
                    flag.append("[P.]")
                    flagcounterP += 1
                elif "[.]" in ligne:
                    flag.append("[.]")
                    flagcounter += 1
                elif "[S]" in ligne:
                    flag.append("[S]")
                    flagcounterS += 1
                if "seq" in ligne:
                    seqcounter += 1
                    seq.append(split[8])
                if "win" in ligne:
                    wincounter += 1
                if "ack" in ligne:
                    ackcounter += 1
                ipsr.append(split[2])
                ipde.append(split[4])
                heure.append(split[0])
                if "length" in ligne:
                    longueur.append(split[-2] if "HTTP" in ligne else split[-1])
                if "ICMP" in ligne:
                    if "request" in ligne:
                        requestcounter += 1
                    elif "reply" in ligne:
                        replycounter += 1

    return (ipsr, ipde, longueur, flag, seq, heure, flagcounterP, flagcounterS, flagcounter, framecounter, 
            requestcounter, replycounter, seqcounter, ackcounter, wincounter)

# Fonction pour calculer les ratios nécessaires
def calculate_ratios(requestcounter, replycounter, flagcounterP, flagcounterS, flagcounter):
    globalreqrepcounter = replycounter + requestcounter
    req = requestcounter / globalreqrepcounter if globalreqrepcounter != 0 else 0
    rep = replycounter / globalreqrepcounter if globalreqrepcounter != 0 else 0

    globalflagcounter = flagcounter + flagcounterP + flagcounterS
    P = flagcounterP / globalflagcounter
    S = flagcounterS / globalflagcounter
    A = flagcounter / globalflagcounter

    return req, rep, P, S, A

# Fonction pour créer un diagramme en barres
def create_bar_chart(data, labels, filename):
    plt.bar(labels, data, color=['blue', 'orange', 'green'])
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart')
    plt.savefig(filename)
    plt.close()

# Fonction pour générer le contenu Markdown
def generate_markdown(framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter):
    markdown_content = f'''
# Choukri

## Projet SAE 15

Sur cette page, nous vous présentons les informations et données pertinentes trouvées dans le fichier à traiter.

### Nombre total de trames échangées
**{framecounter}**

### Drapeaux (Flags)
- Nombre de flags [P] (PUSH) = **{flagcounterP}**
- Nombre de flags [S] (SYN) = **{flagcounterS}**
- Nombre de flag [.] (ACK) = **{flagcounter}**

![Graphe 1](./graphe1.png)

### Nombre de requêtes et réponses
- Request = **{requestcounter}**
- Reply = **{replycounter}**

![Graphe 2](./graphe2.png)

### Statistiques entre seq, win et ack
- Nombre de seq = **{seqcounter}**
- Nombre de win = **{wincounter}**
- Nombre de ack = **{ackcounter}**
'''
    return markdown_content

# Fonction pour sauvegarder les données dans un fichier CSV
def save_csv(filepath, headers, rows):
    try:
        with open(filepath, 'w', newline='') as fichiercsv:
            writer = csv.writer(fichiercsv)
            writer.writerow(headers)
            writer.writerows(rows)
    except PermissionError:
        print(f"Permission denied: {filepath}")
    except Exception as e:
        print(f"An error occurred while saving CSV: {e}")

# Fonction principale
def main():
    try:
        filepath = "C:/Users/userlocal/Desktop/DumpFile.txt"
        ipsr, ipde, longueur, flag, seq, heure, flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter = analyser_fichier(filepath)
        
        req, rep, P, S, A = calculate_ratios(requestcounter, replycounter, flagcounterP, flagcounterS, flagcounter)
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            graphe1_path = os.path.join(tmpdirname, "graphe1.png")
            graphe2_path = os.path.join(tmpdirname, "graphe2.png")
            create_bar_chart([A, P, S], ['Flag [.]', 'Flag [P]', 'Flag [S]'], graphe1_path)
            create_bar_chart([req, rep], ['Request', 'Reply'], graphe2_path)
            
            # Copier les graphiques dans le répertoire de destination
            dest_dir = "C:/Users/userlocal/Desktop/105 sae"
            shutil.copy(graphe1_path, os.path.join(dest_dir, "graphe1.png"))
            shutil.copy(graphe2_path, os.path.join(dest_dir, "graphe2.png"))
            
            # Générer et sauvegarder le contenu Markdown
            markdown_content = generate_markdown(framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter)
            with open(os.path.join(dest_dir, "data1.md"), "w") as md_file:
                md_file.write(markdown_content)
            
            # Sauvegarder les données dans des fichiers CSV
            save_csv(os.path.join(dest_dir, 'donnees1.csv'), ['Heure', 'IP source', 'IP destination', 'Flag', 'Seq', 'Length'], zip(heure, ipsr, ipde, flag, seq, longueur))
            save_csv(os.path.join(dest_dir, 'Stats1.csv'), ['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)', 'Nombre total de trames', 'Nombre de request', 'Nombre de reply', 'Nombre de sequence', 'Nombre de acknowledg', 'Nombre de window'], 
                     [(flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter)])
            
            print("Page Markdown créée avec succès.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()