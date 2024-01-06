import requests
from bs4 import BeautifulSoup
import csv

# URL halaman yang ingin di-scrape
url = "https://pn-sleman.go.id/sipp/list_perkara/type/bjNNT0RNai9WUXE0V2JnR3o0MHRrWTZneU9VNXUrYXdCV1BOZUhyRXY4U3FCRHBnVXRFVm5LUjRPU3VNR2IvbDRrUk9RNTlEN1pIclVUaHlGZTlzM0E9PQ=="

# Mengambil konten HTML dari halaman
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Menemukan elemen tabel
table = soup.find("table")
print("html", soup)

# Mengambil data dari semua kolom dalam tabel
data = []
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if cells:
        row_data = [cell.text for cell in cells]
        data.append(row_data)

# Menyimpan data dalam file CSV
with open("outputtype.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Data berhasil disimpan dalam file outputtype.csv")
