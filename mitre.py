# Importar cliente ATT&CK
from attackcti import attack_client

# Importar bibliotecas adicionales
import pandas as pd
import json
import logging

# Suprimir mensajes innecesarios de taxii2client
logging.getLogger('taxii2client').setLevel(logging.CRITICAL)

# Inicializar cliente ATT&CK
lift = attack_client()

class MITREAttackReporter:
    def __init__(self, lift_client):
        self.lift = lift_client

    def get_techniques(self, export_format):
        techniques = self.lift.get_techniques()
        print("Número de Técnicas en ATT&CK:", len(techniques))
        techniques_list = [json.loads(t.serialize()) for t in techniques]
        self.export_data(techniques_list, "mitre_techniques", export_format)

    def get_groups(self, export_format):
        groups = self.lift.get_groups()
        print("Número de Grupos en ATT&CK:", len(groups))
        groups_list = [json.loads(g.serialize()) for g in groups]
        self.export_data(groups_list, "mitre_groups", export_format)

    def get_software(self, export_format):
        software = self.lift.get_software()
        print("Número de Software en ATT&CK:", len(software))
        software_list = [json.loads(s.serialize()) for s in software]
        self.export_data(software_list, "mitre_software", export_format)

    def get_relationships(self, export_format):
        relationships = self.lift.get_relationships()
        print("Número de Relaciones en ATT&CK:", len(relationships))
        relations_list = [json.loads(r.serialize()) for r in relationships]
        self.export_data(relations_list, "mitre_relationships", export_format)

    def get_data_sources(self, export_format):
        data_sources = self.lift.get_data_sources()
        print("Número de Fuentes de Datos en ATT&CK:", len(data_sources))
        self.export_data(data_sources, "mitre_data_sources", export_format)

    def get_data_components(self, export_format):
        data_components = self.lift.get_data_components()
        print("Número de Componentes de Datos en ATT&CK:", len(data_components))
        self.export_data(data_components, "mitre_data_components", export_format)

    def export_data(self, data, filename, export_format):
        if export_format == "json":
            with open(f"{filename}.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"Reporte exportado a: {filename}.json")
        elif export_format == "txt":
            with open(f"{filename}.txt", "w") as f:
                for item in data:
                    f.write(json.dumps(item, indent=4) + "\n")
            print(f"Reporte exportado a: {filename}.txt")
        elif export_format == "excel":
            df = pd.json_normalize(data)
            df.to_excel(f"{filename}.xlsx", index=False)
            print(f"Reporte exportado a: {filename}.xlsx")
        else:
            print("Formato no válido. No se ha exportado el archivo.")

# Instanciando la clase MITREAttackReporter con el cliente lift
reporter = MITREAttackReporter(lift)

# Menú para interactuar
def main():
    print("""
    ███╗   ███╗██╗████████╗██████╗ ███████╗    █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
    ████╗ ████║██║╚══██╔══╝██╔══██╗██╔════╝   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
    ██╔████╔██║██║   ██║   ██████╔╝█████╗     ███████║   ██║      ██║   ███████║██║     █████╔╝ 
    ██║╚██╔╝██║██║   ██║   ██╔══██╗██╔══╝     ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗ 
    ██║ ╚═╝ ██║██║   ██║   ██║  ██║███████╗   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗
    ╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """)
    print("MITRE ATT&CK Data Exporter - Versión Completa")
    print("--------------------------------------------")
    
    while True:
        print("\nOpciones:")
        print("1. Exportar Técnicas")
        print("2. Exportar Grupos")
        print("3. Exportar Software")
        print("4. Exportar Relaciones")
        print("5. Exportar Fuentes de Datos")
        print("6. Exportar Componentes de Datos")
        print("0. Salir")
        
        choice = input("Seleccione una opción (0-6): ").strip()
        
        if choice == "0":
            print("Saliendo del programa...")
            break
        elif choice in ["1", "2", "3", "4", "5", "6"]:
            # Preguntar el formato de exportación
            export_format = input("¿Cómo desea exportar los datos? (json, txt, excel): ").strip().lower()
            if choice == "1":
                reporter.get_techniques(export_format)
            elif choice == "2":
                reporter.get_groups(export_format)
            elif choice == "3":
                reporter.get_software(export_format)
            elif choice == "4":
                reporter.get_relationships(export_format)
            elif choice == "5":
                reporter.get_data_sources(export_format)
            elif choice == "6":
                reporter.get_data_components(export_format)
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
