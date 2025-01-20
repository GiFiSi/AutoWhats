"""
 1°Passo acessar terminal e selecionar Git Bash

2°Passo executar git add --all para selecionar todas alterações

3°Passo executar git status para verificar esta tudo ok

4°Passo executar git commit -m 'frase desejada'

5°Passo executar git push

6°Passo executar git status verificar se deu tudo certo 

"""

import imaplib
import email
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
import pywhatkit
import time
import subprocess
import threading


# Configuração de logging
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)


# Função para carregar variáveis de ambiente
def load_env_variables():
    load_dotenv()
    return {
        "imap_server": os.getenv("IMAP_SERVER"),
        "email_address": os.getenv("EMAIL_ADDRESS"),
        "password": os.getenv("EMAIL_PASSWORD"),
        "whatsapp_number": os.getenv("WHATSAPP_NUMBER"),
    }


# Função para conectar ao servidor IMAP
def connect_to_imap(imap_server, email_address, password):
    try:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, password)
        return imap
    except Exception as e:
        logging.error(f"Erro ao conectar ao servidor IMAP: {e}")
        sys.exit(1)


# Função para buscar e salvar imagens do email
def fetch_and_save_images(imap, output_directory):
    try:
        imap.select("Inbox")
        today = datetime.now().strftime("%d-%b-%Y")
        search_criteria = f'(FROM "looker-studio-noreply@google.com" SINCE "{today}")'
        _, msgnums = imap.search(None, search_criteria)

        saved_images = []

        for msgnum in msgnums[0].split():
            _, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_bytes(data[0][1])

            logging.info(f"Processando email: {message.get('Subject')}")

            for part in message.walk():
                if part.get_content_type().startswith("image/"):
                    subject = message.get("Subject").replace(" ", "_").replace("/", "_")
                    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{subject}_{date_str}.png"

                    base_filename, extension = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(output_directory, filename)):
                        filename = f"{base_filename}_{counter}{extension}"
                        counter += 1

                    image_path = os.path.join(output_directory, filename)
                    with open(image_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    logging.info(f"Imagem salva: {filename}")
                    saved_images.append(image_path)

        return saved_images
    except Exception as e:
        logging.error(f"Erro ao buscar e salvar imagens: {e}")
        return []


# Função para enviar imagem pelo WhatsApp
def send_whatsapp_image(image_path, whatsapp_number):
    def send_and_exit():
        try:
            caption = "Boa noite a todos!"
            pywhatkit.sendwhats_image(
                whatsapp_number, image_path, caption, 60, True, 10
            )
            logging.info(f"Imagem enviada com sucesso para {whatsapp_number}")
        except Exception as e:
            logging.error(f"Erro ao enviar imagem pelo WhatsApp: {e}")
        finally:
            os._exit(0)

    thread = threading.Thread(target=send_and_exit)
    thread.start()
    thread.join(timeout=900)
    if thread.is_alive():
        logging.warning(
            "O envio da imagem demorou mais que o esperado. Forçando encerramento."
        )
        os._exit(0)


def open_config_editor():
    subprocess.run([sys.executable, "config_editor.py"])


# Função principal
def main():

    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        open_config_editor()
        return

    setup_logging()
    logging.info("Iniciando o programa")

    env_vars = load_env_variables()
    if not all(env_vars.values()):
        logging.error("Variáveis de ambiente não configuradas corretamente")
        sys.exit(1)

    output_directory = os.path.join(
        "Relatorios_diarios", datetime.now().strftime("%Y%m%d")
    )
    os.makedirs(output_directory, exist_ok=True)

    imap = connect_to_imap(
        env_vars["imap_server"], env_vars["email_address"], env_vars["password"]
    )

    saved_images = fetch_and_save_images(imap, output_directory)

    imap.close()
    imap.logout()

    if saved_images:
        for image_path in saved_images:
            send_whatsapp_image(image_path, env_vars["whatsapp_number"])
            time.sleep(60)  # Espera 1 minuto entre cada envio
    else:
        logging.info("Nenhuma imagem encontrada para enviar")

    logging.info("Programa concluído")


if __name__ == "__main__":
    main()
