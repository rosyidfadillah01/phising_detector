import requests
import json
from colorama import Fore, Style
import re

def is_valid_url(url):
    """Fungsi untuk memvalidasi format URL."""
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # Protokol
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
        r'(?::\d+)?'  # Port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def is_valid_email(email):
    """Fungsi untuk memvalidasi format email."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def get_data(api):
    """Fungsi untuk mendapatkan semua data dari API."""
    api_url = api + "/get_data.php"  # Ganti dengan URL API yang sesuai
    try:
        # Mengirim permintaan GET untuk mengambil semua data
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()  # Mengembalikan data dalam format JSON
            return data
        else:
            print(Fore.RED + "Failed to Fetch Data!" + Style.RESET_ALL)
            print("Response:", response.text)
            return None
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))
        return None

def get_email(api):
    """Fungsi untuk mendapatkan semua data dari API."""
    api_url = api + "/get_email.php"  # Ganti dengan URL API yang sesuai
    try:
        # Mengirim permintaan GET untuk mengambil semua data
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()  # Mengembalikan data dalam format JSON
            return data
        else:
            print(Fore.RED + "Failed to Fetch Data!" + Style.RESET_ALL)
            print("Response:", response.text)
            return None
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))
        return None

def insert_or_update_data_phishing(api):
    print(Fore.YELLOW + "\n =============== Insert or Update Data Phishing =============== ")

    url_input = input("Enter URL/Email (ex: https://google.com / halo@gmail.com): ")

    # Validasi input URL atau email
    if is_valid_url(url_input):
        print(Fore.GREEN + "Valid URL!\n" + Style.RESET_ALL)
        
        # Cek apakah data sudah ada
        all_data = get_data(api)

        if all_data:
            # Mencari data berdasarkan URL
            existing_data = next((item for item in all_data if item['url'] == url_input), None)

            if existing_data:
                # Jika data ada, lakukan update
                data_id = existing_data['id']  # Ambil ID dari data yang ada

                status = input("Enter status (1 = true, 0 = false): ")
                # Validasi input status
                if status not in ['0', '1']:
                    print(Fore.RED + "Invalid status! Please enter 1 for true or 0 for false." + Style.RESET_ALL)
                    main()
                    return
                update_data(api, data_id, int(status))
            else:
                status = input("Enter status (1 = true, 0 = false): ")
                # Validasi input status
                if status not in ['0', '1']:
                    print(Fore.RED + "Invalid status! Please enter 1 for true or 0 for false." + Style.RESET_ALL)
                    main()
                    return
                # Jika data tidak ada, lakukan insert
                insert_data(api, url_input, int(status))
        else:
            print(Fore.RED + "Data is NULL !!!" + Style.RESET_ALL)

    elif is_valid_email(url_input):
        print(Fore.GREEN + "Valid Email!\n" + Style.RESET_ALL)

        # Cek apakah data sudah ada
        all_data = get_email(api)

        if all_data:
            # Mencari data berdasarkan URL
            existing_data = next((item for item in all_data if item['email'] == url_input), None)

            if existing_data:
                # Jika data ada, lakukan update
                data_id = existing_data['id']  # Ambil ID dari data yang ada

                status = input("Enter status (1 = true, 0 = false): ")
                # Validasi input status
                if status not in ['0', '1']:
                    print(Fore.RED + "Invalid status! Please enter 1 for true or 0 for false." + Style.RESET_ALL)
                    main()
                    return
                update_email(api, data_id, int(status))
            else:
                status = input("Enter status (1 = true, 0 = false): ")
                # Validasi input status
                if status not in ['0', '1']:
                    print(Fore.RED + "Invalid status! Please enter 1 for true or 0 for false." + Style.RESET_ALL)
                    main()
                    return
                # Jika data tidak ada, lakukan insert
                insert_email(api, url_input, int(status))
        else:
            print(Fore.RED + "Data is NULL !!!" + Style.RESET_ALL)
            main()
    else:
        print(Fore.RED + "Invalid input! Please enter a valid URL or Email.\n" + Style.RESET_ALL)
        main()
        return


def insert_data(api, url, status):
    """Fungsi untuk menyisipkan data baru."""
    data = {
        "url": url,
        "true_false": status
    }

    api_url = api + "/insert_data.php"  # Ganti dengan URL API yang sesuai
    headers = {"Content-Type": "application/json"}

    try:
        # Mengirim permintaan POST
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print(Fore.GREEN + "Data have been Inserted" + Style.RESET_ALL)
            main()
        else:
            print(Fore.RED + "Inserted Failed!" + Style.RESET_ALL)
            print("Response:", response.text)
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))

def insert_email(api, email, status):
    """Fungsi untuk menyisipkan data baru."""
    data = {
        "email": email,
        "true_false": status
    }

    api_email = api + "/insert_email.php"  # Ganti dengan URL API yang sesuai
    headers = {"Content-Type": "application/json"}

    try:
        # Mengirim permintaan POST
        response = requests.post(api_email, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print(Fore.GREEN + "Email have been Inserted" + Style.RESET_ALL)
            main()
        else:
            print(Fore.RED + "Inserted Failed!" + Style.RESET_ALL)
            print("Response:", response.text)
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))

def update_email(api, data_id, status):
    """Fungsi untuk memperbarui data yang sudah ada."""
    data = {
        "id": data_id,
        "true_false": status
    }

    api_url = api + "/update_email.php"  # Ganti dengan URL API yang sesuai
    headers = {"Content-Type": "application/json"}

    try:
        # Mengirim permintaan POST untuk update
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print(Fore.GREEN + "Email Have Been Updated!" + Style.RESET_ALL)
            main()
        else:
            print(Fore.RED + "Fail to Update Email!" + Style.RESET_ALL)
            print("Response:", response.text)

            main()
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))

def update_data(api, data_id, status):
    """Fungsi untuk memperbarui data yang sudah ada."""
    data = {
        "id": data_id,
        "true_false": status
    }

    api_url = api + "/update_data.php"  # Ganti dengan URL API yang sesuai
    headers = {"Content-Type": "application/json"}

    try:
        # Mengirim permintaan POST untuk update
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            main()
            print(Fore.GREEN + "Data Have Been Updated!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Fail to Update Data!" + Style.RESET_ALL)
            print("Response:", response.text)
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))

def search_web(api):
    print(Fore.CYAN + "\n =============== FIND WEBSITE / EMAIL =============== ")
    input_query = input(Fore.YELLOW + "Input URL/Email (ex. https://google.com/usernam@gmail.com) : \n")

    # Mengambil data dan mencari berdasarkan input
    search_results = fetch_and_search(api, input_query)

    # Menampilkan hasil pencarian
    if search_results:
        if search_results["urls"] or search_results["emails"]:
            if search_results["urls"]:
                print(Fore.RED + "This Website is Phising !!!\n" + Style.RESET_ALL)
                main()
            elif search_results["emails"]:
                print(Fore.RED + "This Email is Phising !!!\n" + Style.RESET_ALL)  
                main()
        else:
            print(Fore.GREEN + "This Website & URL is Very Safe\n" + Style.RESET_ALL)
            main()


def fetch_and_search(api, query):
    """Fungsi untuk mengambil data dari API dan mencari berdasarkan query."""
    api_url = api + "/get_all_data.php"  # Ganti dengan URL API yang sesuai
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()  # Mengembalikan data dalam format JSON
            
            results = {
                "urls": [],
                "emails": []
            }

            # Mencari di data pengguna berdasarkan URL
            for user in data.get("urls", []):
                if query.lower() in user.get("url", "").lower():
                    results["urls"].append(user)

            # Mencari di data email
            for email in data.get("emails", []):
                if query.lower() in email.get("email", "").lower():
                    results["emails"].append(email)

            return results
        else:
            print(Fore.RED + "Gagal mengambil data dari API!" + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + "Error:" + Style.RESET_ALL, str(e))
        return None


api = "https://indahkarzatour.com/phising-detector"

def main():
    print(Fore.GREEN + "=========== DETECTOR PHISING ===========")
    print(Fore.GREEN + " ============ By M4TR1X_0N3 ===========\n")
    print(Fore.GREEN + "[1] Insert New Data Phising")
    print(Fore.GREEN + "[2] Search Website / Email Phising")
    key_input = input(Fore.GREEN + "Select Number : ")

    try:
        key_input = int(key_input) # Convert input to integer
        if key_input == 1:
            insert_or_update_data_phishing(api)
        elif key_input == 2 :
            search_web(api)
        else:
            print("Anda tidak memilih 1")
    except ValueError:
        print("Input tidak valid. Masukkan angka.")

    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()

