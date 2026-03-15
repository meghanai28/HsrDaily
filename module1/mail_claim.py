from screen_capture import ScreenCapture
import time
import pyautogui

class MailClaimTask():
    def __init__(self,automation):
        self.auto = automation
        self.mail_with_notif = "icon_mail_with_alert.png"
        self.mail = "icon_mail.png"
        self.claim_all_active = "btn_claim_all_mail.png"
        self.exit_dialog = "dialog_confirm.png"
        self.exit_mail = "exit_mail.png"

    def run(self):
        self.auto.focus_game()
        self.auto.press_key('esc')
        time.sleep(2)
        attempt_mail = self.auto.click_template(self.mail_with_notif, timeout = 3)
        if not attempt_mail:
            attempt_mail = self.auto.click_template(self.mail, timeout = 3)
        if not attempt_mail:
            print("mail clicking failed")
            return False
        self.auto.click_template(self.claim_all_active, timeout = 3)
        self.auto.click_template(self.exit_dialog, timeout = 3)
        exit_attempt = self.auto.click_template(self.exit_mail, timeout = 3)
        if not exit_attempt:
            print("exit mail clicking failed")
            return False
        self.auto.focus_game()
        self.auto.press_key('esc')
        return True

def main():
    engine = ScreenCapture()
    mail_task = MailClaimTask(engine)
    mail_task.run()

if __name__ == "__main__":
    main()