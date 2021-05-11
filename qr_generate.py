import qrcode
code = qrcode.make('ta326')
code.save('ta326.png')
code = qrcode.make('crc235')
code.save('crc235.png')
