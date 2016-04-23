# coding: utf-8

import ui

import random

import clipboard

def mod_pow(a, e, m = 0):

	try:
		if e < 0 :
			print ("Must have e > 0. Please try again.")
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

	for i in range(0,20):
		test_num = random.randint(1,N-1)
		if mod_pow(test_num,N-1,N) == 1:
			correct = correct + 1

	if correct >= 19:
		return N;
	else:
		return 0;

def euclid (a, b):
	if b > a or a < 0 or b < 0 :
		print ('Must have a >= b >= 0')
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
	
	encrypt_view["private_key"].text = str(private_key)
	encrypt_view["big_num0"].text = str(n)
	encrypt_view["big_num1"].text = str(n)
	encrypt_view["public_key"].text = str(public_key)
	
	
	
view = ui.load_view("KeyGen")

if ui.get_screen_size()[1] >= 768:
	# iPad
	view.present()
else:
	# iPhone
	view.present(hide_title_bar=True)