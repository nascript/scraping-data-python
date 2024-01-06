from datetime import datetime

import requests
from bs4 import BeautifulSoup
import csv
import math

# URL halaman yang ingin di-scrape
base_url = "https://pn-sleman.go.id/sipp/list_perkara/page/"
url_key = "/M3FXTExHMGRJVklLWnJGbGZqRksxSTBtOGdLQ1gwSVZnQTlNbWE5SVYrTmI4QlZnUmhvRnY3NGphZUVBUW1id2dQR2RHQkdzVzZJcEt3T0dscnRnTWc9PQ==/key/col/2"


# Menemukan Total Perkara
def get_total_perkara(soup):
    total_perkara_element = soup.find('div', class_='total_perkara')
    if total_perkara_element:
        total_perkara_text = total_perkara_element.get_text(strip=True)
        total_perkara_start = total_perkara_text.find('Total : ') + len('Total : ')
        total_perkara_end = total_perkara_text.find(' Perkara', total_perkara_start)
        total_perkara = total_perkara_text[total_perkara_start:total_perkara_end]

        return total_perkara
    else:
        print("Elemen dengan class 'total_perkara' tidak ditemukan.")
        return None

current_page = 1
header_written = False
timestamp = datetime.now().strftime("%d-%H-%M-%S-%Y")
file_name = f"output-pagination_{timestamp}.csv"


while current_page <= 2:

    url = f"{base_url}{current_page}{url_key}"

    print(f"url {current_page}", url)

    # Mengambil konten HTML dari halaman
    response = requests.get(url)  # Ganti base_url dengan url
    soup = BeautifulSoup(response.content, "html.parser")

    print("html", soup)

    total_perkara_value = get_total_perkara(soup)
    if total_perkara_value is not None:
        print("Total Perkara:", total_perkara_value)

    # Menghitung total halaman
    total_perkara_float = float(total_perkara_value)
    total_page = total_perkara_float / 20
    print("Total Page:", total_page)

    # Menemukan elemen tabel
    table = soup.find("table")

    # Mengambil data dari semua halaman dalam tabel
    data = []

    with open(file_name, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Tulis header hanya pada iterasi pertama
        if current_page == 1 and not header_written:
            header_row = ["No", "Nomor Perkara", "Tanggal Register", "Klasifikasi Perkara", "Para Pihak", "Status Perkara", "Lama Proses", "Link"]
            writer.writerow(header_row)
            header_written = True

        # Mengambil data dari semua halaman dalam tabel
        for idx, row in enumerate(table.find_all("tr")):
            cells = row.find_all("td")
            if cells and idx != 0:  # Skip the first row (header)
                row_data = [cell.text for cell in cells]
                writer.writerow(row_data)

    print(f"save data {current_page} {file_name}")

    current_page += 1
