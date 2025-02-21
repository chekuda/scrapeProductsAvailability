import requests
from bs4 import BeautifulSoup
import json
import datetime

product_file_path_name = "./productUrl.json"

def get_urls_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("proveedores", {})  # Obtener los proveedores y sus URLs
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return {}

def is_text_visible(element):
    """ Verifica si un elemento tiene texto visible y no está oculto por CSS """
    if element.parent.name in ["script", "style", "meta", "head", "title"]:
        return False
    return True  # Si no hay estilo, se asume que es visible

def check_product_availability(urls):
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = {"disponibles": [], "agotados": []}
    
    for url in urls:
        try:
            response = requests.get(url, headers=headers, allow_redirects=False)
            if response.status_code != 200 or response.is_redirect:
                print(f"Redirección detectada o página no disponible: {url}")
                results["agotados"].append(url)
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Detectar si el div principal tiene la clase 'price--sold-out'
            product_div = soup.find("div", class_="price")
            if product_div and "price--sold-out" in product_div.get("class", []):
                results["agotados"].append(url)
                continue
            
            visible_texts = [text.lower() for text in soup.find_all(string=True) if is_text_visible(text)]
        
            if any(keyword in visible_texts for keyword in ["agotado", "sin stock", "sold out"]):
                results["agotados"].append(url)
            else:
                results["disponibles"].append(url)
        except Exception as e:
            results["agotados"].append(url)
    
    return results

if __name__ == "__main__":
    file_path = product_file_path_name  # Archivo JSON con las URLs organizadas por proveedor
    timestamp = datetime.datetime.now().strftime("%H-%M_%d-%m-%Y")
    output_path = f"./resultados/resultados_{timestamp}.json"  # Archivo de salida con marca de tiempo
    proveedores = get_urls_from_json(file_path)
    
    resultados_finales = {"proveedores": {}}
    
    if proveedores:
        for proveedor, data in proveedores.items():
            urls = data.get("urls", [])
            if urls:
                print(f"\nChecking productos for proveedor: {proveedor}\n")
                resultados = check_product_availability(urls)
                resultados_finales["proveedores"][proveedor] = resultados
                for url in resultados["disponibles"]:
                    print(f"{url}: Disponible")
                for url in resultados["agotados"]:
                    print(f"{url}: Agotado")
            else:
                print(f"No se encontraron URLs para el proveedor {proveedor}.")
    else:
        print("No se encontraron proveedores en el archivo JSON.")
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(resultados_finales, outfile, indent=4, ensure_ascii=False)
    print(f"Resultados guardados en {output_path}")

