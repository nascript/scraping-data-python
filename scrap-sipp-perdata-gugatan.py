from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
import math

# URL halaman yang ingin di-scrape
base_url = "https://pn-sleman.go.id/sipp/list_perkara"
pidana_biasa_key = "/type/bjNNT0RNai9WUXE0V2JnR3o0MHRrWTZneU9VNXUrYXdCV1BOZUhyRXY4U3FCRHBnVXRFVm5LUjRPU3VNR2IvbDRrUk9RNTlEN1pIclVUaHlGZTlzM0E9PQ=="
pidana_cepat_key = "/type/NlZEMHVFUURBZmsvYmJwRnVGRW1oU2cva2Y4VVZkUUVBUVM0b0J1ZFNXSmZ3Y1oxeGJZeG9DdVdacStXTHcxbE1YQkJjZElhRGVmcnBEcWI3b1p0cUE9PQ=="
perdata_gugatan_key = "/type/andqMGE2Mlc3WlFDRGMxNlJqcTZpa0tkZThQSGVtcktXWWFiTFdmeGFGV2NZNkJBRFc1ZWVLc3ZVSGxCdnl1UHZZWnRqbGFBSWlZdTJjZk42SEJ5SEE9PQ=="
perdata_permohonan_key = "/type/cFBaZ3RhY0xMRVdzQnJ4U3VUdEphdWJ1YTZsMHJFWlpaaG9oeEREWVVCKzNlSDQ4QUJzc1BLZlpuKzlCQi9WcFNnT3hzWkIybnVRV1pWZzhaZkVDM1E9PQ=="

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
file_name = f"perdata_gugatan_{timestamp}.csv"

url = f"{base_url}{perdata_gugatan_key}"

# Mengambil konten HTML dari halaman
response = requests.get(url)  # Ganti base_url dengan url
soup = BeautifulSoup(response.content, "html.parser")

total_perkara_value = get_total_perkara(soup)
if total_perkara_value is not None:
    print("Total Perkara:", total_perkara_value)

# Menghitung total halaman
total_perkara = total_perkara_value.replace(".", "")
total_page = int(total_perkara) / 20
print("Total Page:", total_page)

while current_page <= total_page:
    url = f"{base_url}/page/{current_page}"

    print(f"url {current_page}", url)

    # Mengambil konten HTML dari halaman
    response = requests.get(url)  # Ganti base_url dengan url
    soup = BeautifulSoup(response.content, "html.parser")

    print("html", soup)

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

    print(f"save data {total_page}/{current_page} {file_name}")

    current_page += 1
