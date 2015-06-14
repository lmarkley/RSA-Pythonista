# coding: utf-8

import ui
import random
import clipboard

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
	
	encoded_message = [0 for i in xrange(0,8192)]

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
	
	clipboard.set(str(result))
	
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
	
def mod_pow(a, e, m = 0):

	try:
		if e < 0 :
			print "Must have e > 0. Please try again."
			raise ValueError
	except: ValueError


	solution = a
	temp = a


	if m == 0 :
		if e == 0 :
			return 1;
		if e == 1 :
			return a;
		if e == 2 : 
			return (a * a);
		if e % 2 == 0 : 
			temp = mod_pow(a, e/2)
			solution = (temp * temp)
			return solution;
		else : 
			temp = mod_pow(temp,e/2)
			solution = ((temp * temp)*a)
			return solution;
	else :
		if e == 0:	
			return 1;
		if e == 1 :
			return a%m;
		if e == 2 : 
			return (a * a) % m;
		if e % 2 == 0 : 
			temp = mod_pow(a, e/2, m)
			solution = (temp * temp) % m
			return solution;
		else : 
			temp = mod_pow(temp,e/2,m)
			solution = (((temp * temp)%m)*a)%m
			return solution;
			
def fermat ( prime_length ):
	if prime_length <= 0:
		return 0;

	N = random.randrange(mod_pow(10,prime_length-1), mod_pow(10,prime_length))

	if (N%2) == 0:
		N += 1

	correct = 0

	for i in xrange(0,20):
		test_num = random.randint(1,N-1)
		if mod_pow(test_num,N-1,N) == 1:
			correct = correct + 1

	if correct >= 19:
		return N;
	else:
		return 0;

def euclid (a, b):
	if b > a or a < 0 or b < 0 :
		print 'Must have a >= b >= 0'
		return [0,0]

	s = 0; old_s = 1;
	t = 1; old_t = 0;
	r = b; old_r = a;

	while ( r != 0 ):
		quotient = old_r / r

		prov_r = r
		r = old_r - quotient * prov_r
		old_r = prov_r

		prov_s = s
		s = old_s - quotient * prov_s
		old_s = prov_s

		prov_t = t
		t = old_t - quotient * prov_t;
		old_t = prov_t

		if ( old_t < 0 ):
			old_t += a;

	return [old_t, old_s]


def keygen_pressed(sender):
	'@type sender:ui.Button'
	
	public_key = int(sender.superview["pub_key"].text)
	
	length = int(sender.superview["prime"].text)
	
	p = 0
	q = 0

	while p == 0:
		p = fermat(length)
		
	while q == 0:
		q = fermat(length)
		
	psi = (p-1)*(q-1)
	
	n = p*q
		
	[private_key, uninteresting] = euclid(psi,public_key)
	
	sender.superview["private_key_out"].text = str(private_key)
	
	sender.superview["big_num_out"].text = str(n)
	
	encrypt_view["RSA_scrollview"]["private_key"].text = str(private_key)
	encrypt_view["RSA_scrollview"]["big_num0"].text = str(n)
	encrypt_view["RSA_scrollview"]["big_num1"].text = str(n)
	encrypt_view["RSA_scrollview"]["public_key"].text = str(public_key)
	
def bring_rsa_forward( sender ):
	'@type sender:ui.Button'
	keygen_view.send_to_back()
	encrypt_view.present(hide_title_bar=True)
	
def bring_keygen_forward( sender ):
	'@type sender:ui.Button'
	encrypt_view.send_to_back()
	keygen_view.present(hide_title_bar=True )
	
def dismiss_view( sender ):
	'@type sender:ui.Button'
	view.close()
	
def dismiss_encrypt( sender ):
	'@type sender:ui.Button'
	encrypt_view.close()
	
def dismiss_keygen( sender ):
	'@type sender:ui.Button'
	keygen_view.close()
	
def get_clip( sender ):
	'@type sender:ui.Button'
	sender.superview["message_to_encrypt"].text = str(clipboard.get())
	
	
view = ui.load_view("RSA_Combined")

encrypt_view = ui.load_view("RSA")
encrypt_view.flex = "WH"

keygen_view = ui.load_view("KeyGen")	
keygen_view.flex = "WH"

if ui.get_screen_size()[1] >= 768:
	view.present(style='full-screen',hide_title_bar=True,orientations='portrait')
else:
	# iPhone
	view.present(style='full-screen',hide_title_bar=True,orientations='portrait')
