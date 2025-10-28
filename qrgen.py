import qrcode, os

def generate_wifi_qrcode(
    ssid: str,
    password: str,
    color: str="black",
    security_type="WPA",
    target: str = "wifi_qrcode.png",
) -> None:
    wifi_data = f"WIFI:T:{security_type};S:{ssid};P:{password};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(wifi_data)
    qr.make(fit=True)

    qr_code_image = qr.make_image(
        fill_color=color, back_color="white"
    )

    qr_code_image.save("qrwifi.png")

def generate_text_qrcode(
    text: str,
    color: str="black",
) -> None:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(text)
    qr.make(fit=True)

    qr_code_image = qr.make_image(
        fill_color=color, back_color="white"
    )

    qr_code_image.save("qrtext.png")

def create_qr_text():
    user_text = input("What is the Text/Web Address:\n> ")
    print("What color do you want it to be (black, green, purple, or red)")

    while True:
        user_color = (str(input("> ")))
        if user_color not in ["black", "green", "purple", "red"]:
            print("Not an accepted color, try again:")
        else:
            break
    generate_text_qrcode(user_text, user_color)

def create_qr_wifi():
    user_ssid = input("What is the name/ssid:\n> ")
    user_pwd = input("What is the wifi password:\n> ")
    print("What color do you want it to be (black, green, purple, blue or red)")

    while True:
        user_color = (str(input("> ")))
        if user_color not in ["black", "green", "purple", "blue", "red"]:
            print("Not an accepted color, try again:")
        else:
            break
    generate_wifi_qrcode(user_ssid, user_pwd, user_color)

def begin_gen():
    print("What type of QR code would you like to create?\n1 = Text/Web Address\n2 = Wifi Login\nq = Quit")
    while True:
        user_input = (input("> "))
        if user_input.lower() == "q":
            os.sys.exit()
        elif user_input == "1":
            create_qr_text()
            break
        elif user_input == "2":
            create_qr_wifi()
            break
        else:
            print("You must select 1, 2, or q.")

    print("QR code generating....SUCCESS!\nQR code image is saved in same folder you ran this program.")
    print("Start over (y/n)?")
    while True:
        start_over = str(input("> "))
        if start_over.lower() == "y":
            begin_gen()
        elif start_over.lower() == "n":
            print("Thank you, please come again!")
            os.sys.exit()
        else:
            print("Must select y or n")

print("Hello user.")
begin_gen()