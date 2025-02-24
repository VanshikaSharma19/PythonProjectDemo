import qrcode
import image
qr = qrcode.QRCode(version=1, error_correction='L')
data = "https://drive.google.com/file/d/1h9Ikogriw9LR45lPg-iM7SS1gAw0OBH6/view?usp=sharing"
#i have given the path of my cv 

qr.add_data(data)
qr.make(fit = True)
img = qr.make_image(fill="black", back_color="white")
img.save("test.png")