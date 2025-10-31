import FreeSimpleGUI as sg
import qrcode
from pathlib import Path


sg.theme('DarkAmber')


# Files to create
TEXT_QR_FILE = Path('qrtext.png')
WIFI_QR_FILE = Path('qrwifi.png')


# Predetermined colors for drop down menu
COLORS = ['Black', 'Red', 'Green', 'Purple', 'Blue', 'Brown', 'Orange']


SECURITY_TYPES = ['WPA', 'WEP', 'nopass']


def generate_qrcode(
   data: str,
   color: str,
   target_filename: Path,
) -> str:
   try:
       qr = qrcode.QRCode(
           version=1,  
           error_correction=qrcode.constants.ERROR_CORRECT_L,
           box_size=5,
           border=4,
       )


       qr.add_data(data)
       qr.make(fit=True)
       qr_code_image = qr.make_image(
           fill_color=color.lower(), back_color="white"
       )


       qr_code_image.save(target_filename)
       return str(target_filename)
   except Exception as e:
       print(f"Error during QR code generation: {e}")
       return None


def generate_wifi_data(ssid: str, password: str, security_type: str) -> str:
   if security_type == 'nopass':
       return f"WIFI:T:nopass;S:{ssid};P:;;"
   else:
       return f"WIFI:T:{security_type};S:{ssid};P:{password};;"


text_tab_layout = [
   [sg.Text('Text or URL to Encode:', size=(18, 1)), sg.Input(key='-TEXT_DATA-', expand_x=True)],
   [sg.Text('QR Code Color:', size=(18, 1)), sg.Combo(COLORS, default_value='Black', key='-TEXT_COLOR-', readonly=True, expand_x=True)],
   [sg.Button('Synthesize Text QR', key='-GENERATE_TEXT-', size=(20, 1), button_color=('white', '#8B4513'))]
]


wifi_tab_layout = [
   [sg.Text('Network Name (SSID):', size=(18, 1)), sg.Input(key='-WIFI_SSID-', expand_x=True)],
   [sg.Text('Password:', size=(18, 1)), sg.Input(key='-WIFI_PASS-', password_char='•', expand_x=True)],
   [sg.Text('Security Type:', size=(18, 1)), sg.Combo(SECURITY_TYPES, default_value='WPA', key='-WIFI_SEC-', readonly=True, expand_x=True)],
   [sg.Text('QR Code Color:', size=(18, 1)), sg.Combo(COLORS, default_value='Black', key='-WIFI_COLOR-', readonly=True, expand_x=True)],
   [sg.Button('Synthesize WiFi QR', key='-GENERATE_WIFI-', size=(20, 1), button_color=('white', '#8B4513'))]
]


text_tab_content = sg.Column(text_tab_layout, element_justification='left')
wifi_tab_content = sg.Column(wifi_tab_layout, element_justification='left')


main_layout = [
   [sg.TabGroup([[
       sg.Tab('Text / URL QR', [[text_tab_content]], key='-TAB_TEXT-'),
       sg.Tab('WiFi Login QR', [[wifi_tab_content]], key='-TAB_WIFI-')
   ]], expand_x=True, key='-TAB_GROUP-')],
   [sg.HorizontalSeparator()],
   [sg.Frame('QR Code Output', [
       [sg.Image(key='-QR_IMAGE-', size=(300, 300), background_color='white')],
       [sg.Text('Enter details and click "Synthesizer" to start.', size=(65, 1), key='-STATUS_MESSAGE-')]
   ], element_justification='center', expand_x=True, expand_y=True)],
   [sg.Button('Exit', button_color=('white', 'red'), key='Exit', expand_x=True, pad=((10, 10), (10, 10)))]
]
window = sg.Window('Professor Maxwell\'s Squarecode Synthesizer', main_layout, finalize=True, size=(460, 620))


def main():
   while True:
       event, values = window.read()


       if event == sg.WIN_CLOSED or event == 'Exit':
           break


       try:
           if event == '-GENERATE_TEXT-':
               data = values['-TEXT_DATA-'].strip()
               color = values['-TEXT_COLOR-']


               if not data:
                   window['-STATUS_MESSAGE-'].update('Error: Text/URL field cannot be empty!', text_color='red')
                   continue


               filepath = generate_qrcode(data, color, TEXT_QR_FILE)
              
               if filepath:
                   window['-QR_IMAGE-'].update(filename=filepath, size=(300, 300))
                   window['-STATUS_MESSAGE-'].update(f'SUCCESS! Text QR code synthesized and saved as {TEXT_QR_FILE.name}')


           elif event == '-GENERATE_WIFI-':
               ssid = values['-WIFI_SSID-'].strip()
               password = values['-WIFI_PASS-']
               security = values['-WIFI_SEC-']
               color = values['-WIFI_COLOR-']


               if not ssid:
                   window['-STATUS_MESSAGE-'].update('Error: SSID field cannot be empty!', text_color='red')
                   continue


               if security in ['WPA', 'WEP'] and not password:
                   window['-STATUS_MESSAGE-'].update(f'Error: Password is required for {security} security type.', text_color='red')
                   continue


               wifi_data = generate_wifi_data(ssid, password, security)
               filepath = generate_qrcode(wifi_data, color, WIFI_QR_FILE)


               if filepath:
                   window['-QR_IMAGE-'].update(filename=filepath, size=(300, 300))
                   window['-STATUS_MESSAGE-'].update(f'SUCCESS! WiFi QR code synthesized and saved as {WIFI_QR_FILE.name}')


       except Exception as e:
           window['-STATUS_MESSAGE-'].update(f'A catastrophic error occurred: {e}', text_color='red')


   window.close()
  
if __name__ == '__main__':
   main()





