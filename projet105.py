import re
from collections import Counter

def read_tcpdump_file(file_path):
  lines = read_tcpdump_file(input_file)
print("Contenu du fichier :")



def extract_packet_info(lines):
    """Extrait les informations pertinentes des lignes du fichier."""
    # Regex mise à jour pour capturer les IP source, port source, IP destination et port destination
    regex = r"IP (\S+)\.(\d+) > (\d+\.\d+\.\d+\.\d+)\.(\d+):"
    results = []
    for line in lines:
        match = re.search(regex, line)
        if match:
            src_ip, src_port, dst_ip, dst_port = match.groups()
            results.append({
                "Source IP": src_ip,
                "Source Port": int(src_port),
                "Destination IP": dst_ip,
                "Destination Port": int(dst_port),
            })
    return results

def analyze_data(results):
    """Analyse les données extraites pour identifier les IP sources et les ports les plus fréquents."""
    src_ip_counts = Counter([entry["Source IP"] for entry in results])
    dst_port_counts = Counter([entry["Destination Port"] for entry in results])
    return src_ip_counts, dst_port_counts

# Main script
if __name__ == "__main__":
    input_file = "C:/Users/userlocal/Downloads/tcpfile2.txt"  # Remplacez par le chemin de votre fichier tcpdump

    # Lire les lignes du fichier tcpdump
    lines = read_tcpdump_file(input_file)

    # Extraire les informations des paquets
    results = extract_packet_info(lines)

    # Analyser les données
    src_ip_counts, dst_port_counts = analyze_data(results)

    # Afficher les résultats d'analyse
    print("\nTop IP sources :")
    for ip, count in src_ip_counts.most_common(5):
        print(f"IP : {ip}, Connexions : {count}")

    print("\nTop ports de destination :")
    for port, count in dst_port_counts.most_common(5):
        print(f"Port : {port}, Connexions : {count}")
