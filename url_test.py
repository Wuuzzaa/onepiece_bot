import requests
import smtplib
from email.mime.text import MIMEText

BASE_URL_START = "http://onepiece-tube.com/kapitel/"
BASE_URL_END = "/1"
FILE_NAME = "CHAPTER_NR.txt"

EMAILS = ["jonas-licht@gmx.de", "tunnelfighter@web.de"]


def read_chapter_nr(file_name):
    with open(file_name, "r") as f:
        return f.read()


def write_chapter_nr(file_name, text):
    with open(file_name, "w") as f:
        print("Write: {} to file: {}".format(text, file_name))
        f.write(text)


def generate_url(start, chapter,  end):
    return start + chapter + end


def exists(url):
    try:
        r = requests.head(url)
        return r.status_code == 200  # 200 ist HTTP OK Status
    except Exception as ex:
        print(ex)
        return False


def send_mails(chapter, EMAILS):
    for email in EMAILS:
        send_mail(chapter, email)


def send_mail(chapter, email):
    print("E-Mail senden an: {} ".format(email))

    senderEmail = "OnePieceBot@gmx.de"
    empfangsEmail = email
    msg = MIMEText("Ahoi, Kapitel {} ist raus gogogo...".format(chapter))
    msg['From'] = senderEmail
    msg['To'] = empfangsEmail
    msg['Subject'] = "One Piece neues Kapitel ist raus"

    server = smtplib.SMTP('mail.gmx.net', 587)  # Die Server Daten
    server.starttls()
    server.login(senderEmail, "botbotbot")  # Das Passwort
    text = msg.as_string()
    server.sendmail(senderEmail, empfangsEmail, text)
    server.quit()

current_chapter = read_chapter_nr(FILE_NAME)
next_chapter = str(int(current_chapter) + 1)
url = generate_url(BASE_URL_START, next_chapter, BASE_URL_END)

if exists(url):
    print("Neues Kapitel online! Aktuellest Kapitel ist {}".format(next_chapter))
    # Mails senden
    send_mails(next_chapter, EMAILS)
    # File aktualisieren
    write_chapter_nr(FILE_NAME, next_chapter)

else:
    print("Kein neues Kapitel online! Aktuellest Kapitel ist {}".format(current_chapter))
