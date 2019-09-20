
from .models import *
from .constants import * 
import datetime

def encrypt(client_id,bureau_id,total_amount,date,rate):
	data = f"{client_id,bureau_id,total_amount,date,rate}"
	encodedBytes = base64.b64encode(data.encode("utf-8")).decode()
	return encodedBytes

def decrypt(ciphertext):
	plaintext = base64.b64decode(ciphertext)
	plaintext = plaintext.decode("utf-8")
	plaintext = plaintext[1:-1].split(",")
	plaintext = [text.replace("'","") for text in plaintext]
	return plaintext


def get_currencies(amount, currency_a, currency_b, client_id):
	rates = Rates.get_db_currencies(currency_a, currency_b)	
	highest_rate = 0
	highest_rate_provider = 0
	for rate in rates:
		if rate.rate > highest_rate:
			print(rate.rate)
			highest_rate = rate.rate
			highest_rate_provider = rate.bureau_id	
	if highest_rate == 0: 
		return "No rate for this selection"
	else: 		
		bureau = Bureau.get_by_id(highest_rate_provider)
		if bureau is not None:
			bureau_name,  bureau_address= bureau.name , bureau.address
		else: 
			return "bureau was not found"
		total_amount = float(amount) * float(highest_rate)
		response_message = rate_response_message.format(bureau_name, bureau_address, '0774231343', highest_rate, amount, total_amount)
		transaction = Transaction(client_id=client_id, bureau_id=bureau.id, amount=amount, total_amount=total_amount, rate=highest_rate, transaction_type='internal transfer', date=datetime.datetime.now(), reference_number='12345')
		transaction.save_to_db()		
		return response_message

#print(get_currencies('1', 'USD', 'ZWL'))

def confirm_transaction(confirmation, id):
	if confirmation:
		#complete_transaction
		tran = Transaction.get_by_id(id)
		if tran.client_id is None:
			return "Please Start The Registration Process"
		if tran:
			print(tran.client_id)
			ref_no = encrypt(tran.client_id, tran.bureau_id,\
			tran.total_amount, tran.date, tran.rate)	
			tran.transaction_code = ref_no
			tran.save_to_db()		 
			confirmation_message = transaction_confirmation_message.format(ref_no)
			return confirmation_message	
		else:
			return "Transaction Not Found"
				 
	return "Transaction Cancelled"





