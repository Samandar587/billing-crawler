import requests
import tempfile
import subprocess
import os
import platform

base_url = "https://billing.sud.uz/api/invoice"
create_invoice_url = base_url + "/create"

data = {
    "entityType": "JURIDICAL",
    "juridicalEntity": {
        "name": "KT IMAN HALAL INVESTMENTS KOMMANDITNOE TOVARISHESTVO",
        "tin": "307128450",
        "address": "Тошкент шаҳар, Миробод тумани, Мирабадский район, улица Шахрисабз, дом 16"
    },
    "amount": 1700000,
    "payCategoryId": 3,
    "overdue": 0,
    "courtType": "CITIZEN",
    "courtId": "528",
    "description": "",
    "isInFavor": True
}

res = requests.post(create_invoice_url, json=data)

if res.status_code == 201:
    res_json = res.json()
    invoice = res_json.get("invoice")
    pdf_url = f"{base_url}/asDocument?invoice={invoice}"
    
    pdf_res = requests.get(pdf_url)
    
    if pdf_res.status_code == 200:
        pdf_content = pdf_res.content
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file_path = temp_file.name
            with open(temp_file_path, "wb") as f:
                f.write(pdf_content)
        
        if platform.system() == "Windows":
            subprocess.Popen(["start", "", temp_file_path], shell=True)
        elif platform.system() == "Linux":
            print(temp_file_path)
            subprocess.Popen(["xdg-open", "/tmp/"+temp_file_path])
        
        if platform.system() == "Windows":
            subprocess.Popen(["AcroRd32.exe", "/t", temp_file_path])
        elif platform.system() == "Linux":
            subprocess.Popen(["evince", "-p", temp_file_path])
        
        os.remove(temp_file_path)
        
    else:
        print("Failed to fetch PDF:", pdf_res.status_code)
else:
    print("Failed to create invoice:", res.status_code)
