from bs4 import BeautifulSoup as pr
import requests
import config
import json


def get_all_work():
    headers = {
        "user-agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58"
    }

    login_url = 'your_url_login'
    secure_url = 'url_for_all_work_page'

    payload = {
        'username': config.username,
        'password': config.password
    }
    s = requests.session()
    s.post(login_url, data=payload, headers=headers)
    r = s.get(secure_url)
    soup = pr(r.text, 'lxml')
    work_new = soup.find('tbody')
    work_list = work_new.find_all('tr')

    work_dict = {}
    for work in work_list:
        work_ID = work.find('td', class_='column-id').text.strip()
        work_iss = work.find('td', class_='column-summary').text.strip()
        work_iss_des = work.find('td', class_='column-description').text.strip()
        work_user = work.find('td', class_='column-custom-Контактна особа (П.І.Б.)').text.strip()
        work_phone = work.find('td', class_='column-custom-Телефон контактної особи').text.strip()
        work_adr = work.find('td', class_='column-custom-Адреса (фактична)').text.strip()
        work_status = work.find('td', class_='column-status').text.strip()
        work_sender = work.find('td', class_='column-reporter').text.strip()
        # print(f"{work_ID} | {work_iss} | {work_user} | {work_phone} | {work_status} | {work_adr}")
        work_dict[work_ID] = {
            "work_sender": work_sender,
            "work_ID": work_ID,
            "work_iss": work_iss,
            "work_iss_des": work_iss_des,
            "work_user": work_user,
            "work_phone": work_phone,
            "work_adr": work_adr,
            "work_status": work_status,
        }
    with open("work_dict.json", "w") as f:
        json.dump(work_dict, f, indent=4, ensure_ascii=False)


def check_new_work():
    with open("work_dict.json") as f:
        work_dict = json.load(f)

        headers = {
            "user-agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58"
        }

        payload = {
            'username': config.username,
            'password': config.password
        }
        s = requests.session()
        s.post(login_url, data=payload, headers=headers)
        r = s.get(secure_url)
        soup = pr(r.text, 'lxml')
        work_new = soup.find('tbody')
        work_list = work_new.find_all('tr')

        new_work_dict = {}
        for work in work_list:
            work_ID = work.find('td', class_='column-id').text.strip()

            if work_ID in work_dict:
                continue
            else:
                work_iss = work.find('td', class_='column-summary').text.strip()
                work_iss_des = work.find('td', class_='column-description').text.strip()
                work_user = work.find('td', class_='column-custom-Контактна особа (П.І.Б.)').text.strip()
                work_phone = work.find('td', class_='column-custom-Телефон контактної особи').text.strip()
                work_adr = work.find('td', class_='column-custom-Адреса (фактична)').text.strip()
                work_status = work.find('td', class_='column-status').text.strip()
                work_sender = work.find('td', class_='column-reporter').text.strip()
                work_dict[work_ID] = {
                    "work_sender": work_sender,
                    "work_ID": work_ID,
                    "work_iss": work_iss,
                    "work_iss_des": work_iss_des,
                    "work_user": work_user,
                    "work_phone": work_phone,
                    "work_adr": work_adr,
                    "work_status": work_status
                }

                new_work_dict[work_ID] = {
                    "work_sender": work_sender,
                    "work_ID": work_ID,
                    "work_iss": work_iss,
                    "work_iss_des": work_iss_des,
                    "work_user": work_user,
                    "work_phone": work_phone,
                    "work_adr": work_adr,
                    "work_status": work_status
                }
            with open("work_dict.json", "w") as file:
                json.dump(work_dict, file, indent=4, ensure_ascii=False)

        return new_work_dict


def check_work_status():
    with open("work_dict.json") as file:
        work_dict = json.load(file)

        headers = {
            "user-agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58"
        }
        payload = {
            'username': config.username,
            'password': config.password
        }
        s = requests.session()
        s.post(login_url, data=payload, headers=headers)
        r = s.get(secure_url)
        soup = pr(r.text, 'lxml')
        work_new = soup.find('tbody')
        work_list = work_new.find_all('tr')

        new_work_status = {}
        for work in work_list:
            work_status = work.find('td', class_='column-status').text.strip()

            if work_status in work_dict:
                continue
            else:
                work_ID = work.find('td', class_='column-id').text.strip()
                work_iss = work.find('td', class_='column-summary').text.strip()
                work_iss_des = work.find('td', class_='column-description').text.strip()
                work_user = work.find('td', class_='column-custom-Контактна особа (П.І.Б.)').text.strip()
                work_phone = work.find('td', class_='column-custom-Телефон контактної особи').text.strip()
                work_adr = work.find('td', class_='column-custom-Адреса (фактична)').text.strip()
                work_sender = work.find('td', class_='column-reporter').text.strip()

                work_dict[work_ID] = {
                    "work_sender": work_sender,
                    "work_ID": work_ID,
                    "work_iss": work_iss,
                    "work_iss_des": work_iss_des,
                    "work_user": work_user,
                    "work_phone": work_phone,
                    "work_adr": work_adr,
                    "work_status": work_status
                }

                new_work_status[work_ID] = {
                    "work_sender": work_sender,
                    "work_ID": work_ID,
                    "work_iss": work_iss,
                    "work_iss_des": work_iss_des,
                    "work_user": work_user,
                    "work_phone": work_phone,
                    "work_adr": work_adr,
                    "work_status": work_status,
                }
            with open("work_dict.json", "w") as f:
                json.dump(work_dict, f, indent=4, ensure_ascii=False)
        return new_work_status


def main():
    get_all_work()
    print(check_work_status())


if __name__ == '__main__':
    main()
