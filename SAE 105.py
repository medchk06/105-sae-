import csv
import webbrowser
import matplotlib.pyplot as plt
import os
import tempfile

def parse_file(filepath):
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

def calculate_ratios(requestcounter, replycounter, flagcounterP, flagcounterS, flagcounter):
    globalreqrepcounter = replycounter + requestcounter
    req = requestcounter / globalreqrepcounter if globalreqrepcounter != 0 else 0
    rep = replycounter / globalreqrepcounter if globalreqrepcounter != 0 else 0

    globalflagcounter = flagcounter + flagcounterP + flagcounterS
    P = flagcounterP / globalflagcounter
    S = flagcounterS / globalflagcounter
    A = flagcounter / globalflagcounter

    return req, rep, P, S, A

def create_pie_chart(data, labels, filename):
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    plt.savefig(filename)
    plt.close()

def generate_html(framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter):
    html_content = '''
    <html lang="fr">
       <head>
          <meta charset="UTF-8">
          <title> Traitement des données </title>
          <style>
          body{
              background-image: url('https://www.codeur.com/blog/wp-content/uploads/2021/08/image-programmation-1.jpg');
              background-repeat: no-repeat;
              background-size: cover;
              color:#e5f2f7;
              background-attachment: fixed;
              }
          </style>
       </head>
       <body>
           <center><h1>Choukri</h1></center>
           <center><h2>Projet SAE 15</h2></center>
           <center><p>Sur cette page web, nous vous présentons les informations et données pertinentes trouvées dans le fichier à traiter.</p></center>
           <center><h3> Nombre total de trames échangées</h3> %s</center>
           <br>
           <center><h3> Drapeaux (Flags)<h3></center>
           <center>Nombre de flags [P] (PUSH) = %s
           <br>Nombre de flags [S] (SYN) = %s  
           <br>Nombre de flag [.] (ACK) = %s
           <br>
           <br>
           <img src="graphe1.png">
           <h3> Nombre de requêtes et réponses </h3>
           Request = %s 
           <br>
           Reply = %s
           <br>
           <br>
           <img src="graphe2.png">
           <h3>Statistiques entre seq, win et ack </h3>
           Nombre de seq = %s
           <br>
           Nombre de win = %s
           <br>
           Nombre de ack = %s
       </body>
    </html>
    ''' % (framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter)
    return html_content

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

def main():
    try:
        filepath = "C:/Users/userlocal/Desktop/DumpFile.txt"
        ipsr, ipde, longueur, flag, seq, heure, flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter = parse_file(filepath)
        
        req, rep, P, S, A = calculate_ratios(requestcounter, replycounter, flagcounterP, flagcounterS, flagcounter)
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            create_pie_chart([A, P, S], ['Flag [.]', 'Flag [P]', 'Flag [S]'], os.path.join(tmpdirname, "graphe1.png"))
            create_pie_chart([req, rep], ['Request', 'Reply'], os.path.join(tmpdirname, "graphe2.png"))
            
            html_content = generate_html(framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter)
            with open("C:/Users/userlocal/Desktop/105 sae/data1.html", "w") as html:
                html.write(html_content)
            
            save_csv('C:/Users/userlocal/Desktop/105 sae/donnees1.csv', ['Heure', 'IP source', 'IP destination', 'Flag', 'Seq', 'Length'], zip(heure, ipsr, ipde, flag, seq, longueur))
            save_csv('C:/Users/userlocal/Desktop/105 sae/Stats1.csv', ['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)', 'Nombre total de trames', 'Nombre de request', 'Nombre de reply', 'Nombre de sequence', 'Nombre de acknowledg', 'Nombre de window'], 
                     [(flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter)])
            
            print("Page web créée avec succès.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()