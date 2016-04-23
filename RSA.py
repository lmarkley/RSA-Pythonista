# coding: utf-8

import ui


def rsa_encrypt( message, n = 17032829174044515277, e = 137):
	m_length = len(message)
	ciphertext = ''
	ascii_message = [ 0 for i in xrange(0,m_length)]
	
	
	for i in xrange(0,m_length):
		ascii_message[i] = ord(message[i])
		
		
	word_count = 1
	phrase = ascii_message[0]
	for c in xrange(1,m_length):
		phrase = 256*phrase + ascii_message[c]
		
		if c == word_count * 2 - 1 or c == m_length-1 :
			encrypted_string = str(pow(phrase,e,n))
			while len(encrypted_string) < 25 :
				encrypted_string = str("0") + encrypted_string
			ciphertext += encrypted_string
			encrypted_string = ''
			word_count += 1
			phrase = 0
		
	return ciphertext

def rsa_decrypt( message, d = 1616253862289875993, n = 17032829174044515277):
	
	m_length = len(message)
	
	encoded_message = [0 for i in xrange(0,1024)]

	encoded_message_string = ''

	char_num = 0
	phrase_num = 1

	while char_num < m_length :
		encoded_message_string += message[char_num]
	
		if char_num == 25 * phrase_num - 1 :
			encoded_message[phrase_num] = int(encoded_message_string)
			encoded_message_string = ''
			phrase_num += 1

		char_num += 1

	result = ''

	reversed_decoded_message = ['' for j in xrange(0,phrase_num)]

	for i in xrange(0,phrase_num) :

		decrypted_base128 = pow(encoded_message[i],d,n)

		decoded_message = ''

		while decrypted_base128 != 0 :
			temp = decrypted_base128 % 256
			decrypted_base128 = decrypted_base128 / 256
			decoded_ascii_char = chr(temp)
			decoded_message += decoded_ascii_char

		reversed_decoded_message[i] += decoded_message[::-1]

	for k in xrange(0,phrase_num):
		result += reversed_decoded_message[k]

	return result

def encrypt_pressed(sender):
	'@type sender:ui.Button'
	message = sender.superview["message_to_encrypt"].text
	
	pubkey = int(sender.superview["public_key"].text)
	
	n = int(sender.superview["big_num0"].text)
	
	result = ''
	
	result = rsa_encrypt( message, n, pubkey )
	sender.superview["encrypted_message"].text = result
	
def decrypt_pressed(sender):
	'@type sender:ui.Button'
	message = sender.superview["message_to_decrypt"].text
	
	private = int(sender.superview["private_key"].text)
	
	n = int(sender.superview["big_num1"].text)
	
	result = ''
	
	result = rsa_decrypt( message, private, n )
	sender.superview["decrypted_message"].text = result
	
def encrypted_to_decrypt( sender ):
	'@type sender:ui.Button'
	sender.superview["message_to_decrypt"].text = sender.superview["encrypted_message"].text
	

	
view = ui.load_view("RSA")

if ui.get_screen_size()[1] >= 768:
	# iPad
	view.present('popover')
else:
	# iPhone
	view.present(hide_title_bar=True)