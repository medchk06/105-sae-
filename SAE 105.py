import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import os
import tempfile
import shutil
import markdown
import webbrowser
from tkinter import font as tkfont

# Fonction pour analyser le fichier et extraire les informations pertinentes
def analyser_fichier(filepath):
    with open(filepath, "r") as fichier:
        issues = []
        packet_counts = {
            "DNS NXDomain": 0,
            "Suspicious SYN": 0,
            "Repeated Payload": 0,
            "Total Packets": 0
        }

        file_content = fichier.read()

        # Compter le nombre total de paquets
        all_packets_pattern = re.compile(r"^\d+", re.MULTILINE)
        all_packets = all_packets_pattern.findall(file_content)
        packet_counts["Total Packets"] = len(all_packets)

        # Rechercher des paquets suspects
        dns_frames = list(set(re.findall(r".*NXDomain.*", file_content, re.MULTILINE)))
        syn_frames = list(set(re.findall(r"IP \S+ > \S+\.http: Flags \[S\].*?", file_content)))
        repeated_frames = list(set(re.findall(r".*5858 5858.*", file_content)))

        # Mettre à jour les compteurs de paquets
        packet_counts["DNS NXDomain"] = len(dns_frames)
        packet_counts["Suspicious SYN"] = len(syn_frames)
        packet_counts["Repeated Payload"] = len(repeated_frames)

        # Stocker les détails des paquets suspects
        for frame in dns_frames:
            issues.append(["DNS Error", "DNS Resolution Failed", frame])

        for frame in syn_frames:
            issues.append(["SYN Flag", "Suspicious SYN Connection", frame])

        for frame in repeated_frames:
            issues.append(["Repetition", "Repeated Payload Data", frame])

    return issues, packet_counts

# Fonction pour générer un rapport CSV
def generer_csv(issues, filepath):
    try:
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as fichiercsv:
            writer = csv.writer(fichiercsv, delimiter=';')
            writer.writerow(["Type", "Description", "Frame"])
            writer.writerows(issues)
        messagebox.showinfo("Success", "Results saved into a CSV file.")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to save the file: {e}")

# Fonction pour générer un rapport HTML
def generer_html(issues, packet_counts):
    # Convertir les résultats en contenu Markdown
    markdown_content = "| Type | Description | Frame |\n"
    markdown_content += "| ---  | ---         | ---   |\n"

    for issue in issues:
        markdown_content += f"| {issue[0]} | {issue[1]} | {issue[2]} |\n"

    html_converted_content = markdown.markdown(markdown_content, extensions=['tables'])

    # Créer un graphique en barres
    fig, ax = plt.subplots(figsize=(12, 8))  # Increased size of the graph
    bars = ax.bar(packet_counts.keys(), packet_counts.values(), color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])  # Customized colors
    ax.set_title("Packet Distribution", fontsize=16, fontweight='bold')  # Customized font
    ax.set_xlabel("Issue Types", fontsize=14)
    ax.set_ylabel("Number of Packets", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)  # Added grid lines
    plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)

    # Add value labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontsize=12)

    # Sauvegarder le graphique en tant qu'image
    bar_chart_filename = "bar_chart.png"
    bar_chart_full_path = os.path.join(tempfile.gettempdir(), bar_chart_filename)
    fig.savefig(bar_chart_full_path)
    plt.close(fig)

    # Générer le contenu HTML final
    final_html_content = f"""
    <html>
    <head>
    <title>TCP Analysis Report</title>
        <style>
            body {{ font-family: 'Verdana', sans-serif; background-color: #f0f0f0; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            h1 {{ color: #4CAF50; }}
            h2 {{ color: #333; }}
            .navbar {{ overflow: hidden; background-color: #333; }}
            .navbar a {{ float: left; display: block; color: #f2f2f2; text-align: center; padding: 14px 16px; text-decoration: none; }}
            .navbar a:hover {{ background-color: #ddd; color: black; }}
            .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; background-color: #333; color: white; text-align: center; padding: 10px 0; }}
            .container {{ max-width: 1200px; margin: auto; padding: 20px; }}
            .content {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <a href="#results">Results</a>
            <a href="#chart">Chart</a>
        </div>
        <div class="container">
            <div class="content">
                <h1 id="results">TCP Analysis Results</h1>
                {html_converted_content}
                <h2 id="chart">Packet Distribution</h2>
                <img src="{bar_chart_filename}" alt="Bar Chart" width="800" />  <!-- Increased width of the image -->
            </div>
        </div>
    </body>
    </html>
    """

    # Sauvegarder le fichier HTML
    html_filepath = os.path.join(tempfile.gettempdir(), "tcp_analysis.html")
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(final_html_content)

    # Ouvrir le fichier HTML dans le navigateur
    webbrowser.open('file://' + html_filepath)

# Fonction pour générer un rapport Markdown
def generer_markdown(issues, packet_counts):
    markdown_content = "# TCP Analysis Results\n\n"
    markdown_content += "## Packet Counts\n"
    for key, value in packet_counts.items():
        markdown_content += f"- **{key}**: {value}\n"

    markdown_content += "\n## Issues Detected\n"
    markdown_content += "| Type | Description | Frame |\n"
    markdown_content += "| ---  | ---         | ---   |\n"

    for issue in issues:
        markdown_content += f"| {issue[0]} | {issue[1]} | {issue[2]} |\n"

    return markdown_content

# Fonction principale pour charger un fichier et afficher les résultats
def charger_fichier():
    filepath = filedialog.askopenfilename()
    if filepath:
        try:
            issues, packet_counts = analyser_fichier(filepath)
            afficher_resultats(issues, packet_counts)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to analyze the file: {e}")

# Fonction pour afficher les résultats dans une nouvelle fenêtre
def afficher_resultats(issues, packet_counts):
    results_window = tk.Toplevel()
    results_window.title("Analysis Results")
    results_window.geometry("800x600")

    # Créer un Treeview pour afficher les résultats
    tree = ttk.Treeview(results_window)
    tree["columns"] = ("Type", "Description", "Frame")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Type", anchor=tk.W, width=120)
    tree.column("Description", anchor=tk.W, width=200)
    tree.column("Frame", anchor=tk.W, width=400)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Type", text="Type", anchor=tk.W)
    tree.heading("Description", text="Description", anchor=tk.W)
    tree.heading("Frame", text="Suspicious Frame", anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True)

    for issue in issues:
        tree.insert("", tk.END, values=issue)

    # Boutons pour sauvegarder les résultats
    button_frame = ttk.Frame(results_window)
    button_frame.pack(pady=10)

    save_csv_button = tk.Button(button_frame, text="Save as CSV", 
                                command=lambda: generer_csv(issues, filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])))
    save_csv_button.pack(side=tk.LEFT, padx=5)

    save_html_button = tk.Button(button_frame, text="Open in Browser", 
                                 command=lambda: generer_html(issues, packet_counts))
    save_html_button.pack(side=tk.LEFT, padx=5)

    save_md_button = tk.Button(button_frame, text="Save as Markdown", 
                               command=lambda: sauvegarder_markdown(issues, packet_counts))
    save_md_button.pack(side=tk.LEFT, padx=5)

# Fonction pour sauvegarder un rapport Markdown
def sauvegarder_markdown(issues, packet_counts):
    markdown_content = generer_markdown(issues, packet_counts)
    filepath = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            messagebox.showinfo("Success", "Results saved into a Markdown file.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save the file: {e}")

# Interface graphique principale
root = tk.Tk()
root.title("TCP Packet Analyzer")
root.configure(bg='lightgray')

# Utiliser une police personnalisée
custom_font = tkfont.Font(family="Arial", size=12, weight="bold")  # Customized font

btn = tk.Button(root, text="Load a File", command=charger_fichier, 
                font=custom_font, bg='red', fg='white', padx=20, pady=10)  # Changed button color
btn.pack(pady=20)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    root.destroy()