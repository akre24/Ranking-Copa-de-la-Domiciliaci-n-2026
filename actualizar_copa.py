#!/usr/bin/env python3
"""
Script para actualizar la Copa de la Domiciliación desde un archivo CSV
"""

import csv
import re

def leer_csv(archivo_csv):
    """Lee el archivo CSV y retorna una lista de asesores"""
    asesores = []
    with open(archivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nombre = row.get('Nombre', '').strip()
            domiciliaciones = row.get('Domiciliaciones', '0').strip()
            
            if nombre:
                asesores.append({
                    'nombre': nombre,
                    'domiciliaciones': int(domiciliaciones) if domiciliaciones.isdigit() else 0
                })
    return asesores

def generar_javascript(asesores):
    """Genera el código JavaScript con los datos de asesores"""
    js_code = "        const datosAsesores = [\n"
    
    for asesor in asesores:
        js_code += f'            {{nombre: "{asesor["nombre"]}", domiciliaciones: {asesor["domiciliaciones"]}}},\n'
    
    js_code += "        ];"
    return js_code

def actualizar_html(archivo_html, asesores):
    """Actualiza el archivo HTML con los nuevos datos"""
    with open(archivo_html, 'r', encoding='utf-8') as file:
        contenido = file.read()
    
    # Generar nuevo código JavaScript
    nuevo_js = generar_javascript(asesores)
    
    # Patrón para encontrar la sección de datos
    patron = r'        const datosAsesores = \[.*?\];'
    
    # Reemplazar los datos
    contenido_actualizado = re.sub(patron, nuevo_js, contenido, flags=re.DOTALL)
    
    # Guardar el archivo actualizado
    with open(archivo_html, 'w', encoding='utf-8') as file:
        file.write(contenido_actualizado)
    
    print(f"✅ Archivo HTML actualizado exitosamente!")
    print(f"📊 Total de asesores: {len(asesores)}")
    print(f"📈 Total de domiciliaciones: {sum(a['domiciliaciones'] for a in asesores)}")

def main():
    """Función principal"""
    print("🏆 Copa de la Domiciliación 2026 - Actualizador")
    print("=" * 50)
    
    archivo_csv = "datos.csv"
    archivo_html = "copa_domiciliacion_embebido.html"
    
    try:
        # Leer datos del CSV
        print(f"📂 Leyendo datos de: {archivo_csv}")
        asesores = leer_csv(archivo_csv)
        
        if not asesores:
            print("⚠️  No se encontraron asesores en el archivo CSV")
            return
        
        # Actualizar HTML
        print(f"🔄 Actualizando archivo: {archivo_html}")
        actualizar_html(archivo_html, asesores)
        
        print("\n✨ ¡Listo! Ahora puedes abrir el archivo HTML en tu navegador")
        
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontró el archivo - {e}")
        print("Asegúrate de que 'datos.csv' y 'copa_domiciliacion_embebido.html' estén en la misma carpeta")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
