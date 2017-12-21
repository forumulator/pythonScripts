import urllib
from urllib import request, parse
import re
import os, sys
import time
import argparse

# Request headers
headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36', 
			'Referer': 'http://www.verifyemailaddress.org', 
			'Origin': 'http://www.verifyemailaddress.org/',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		  }


class EmailVerifier:
	SITE_URL = 'https://www.verifyemailaddress.org/#result'
	INVALID_SEARCH_STRING = "is not valid"
	CONNECTING_TO_DOMAIN = "Connecting to {0} failed"

	def create_request(self, email_addr):
		post_form = { "email": email_addr }
		enc_data = parse.urlencode(post_form).encode()
		req = request.Request(
			EmailVerifier.SITE_URL,
			data = enc_data,
			headers = headers
		)

		return req

	def check_domain(self, domain):
		req = self.create_request("help@{0}".format(domain))
		resp = request.urlopen(req)
		html = resp.read().decode("utf-8")
		domain_invalid = EmailVerifier.CONNECTING_TO_DOMAIN.format(
			domain) in html
		if domain_invalid:
			print(EmailVerifier.CONNECTING_TO_DOMAIN.format(
			domain))
			return False
		else:
			return True

	# Returns a boolean value
	def verify(self, email_addr, super_verbose = False):
		req = self.create_request(email_addr)
		resp = request.urlopen(req)
		html = resp.read().decode("utf-8")
		if super_verbose:
			print(html)
		re_res = EmailVerifier.INVALID_SEARCH_STRING in html
		return (False if re_res else True)
		# if super_verbose:
		#     print(re_res)

# Possible templates for different sizes
# All the possible combinations are covered by
# this and the action of the Permutator
email_templates = {
	2: [
		"{f}.{l}",
		"{f}{l}",
	],
	3: [
		"{f}{m}{l}",
		"{f}{m}.{l}",
		"{f}.{m}{l}",
		"{f}.{m}.{l}"
	],
	1: [ "{f}" ]
}

EMAIL_FORMAT = "{user}@{domain}"

class Permutator:
	""" Generate all possible combination of two and three
	words to form an email. For example, (first, last), (last, first), (f, last)

	The elems is produced and Permutator is called in a way such that
	the emails are always produced most to least specific
	eg first.last@ before f.last@ before first@
	"""
	def __init__(self, elems):
		self.elems = elems

	# Make actual permutations of elems
	def make_perms(self, elems, r):
		if r == 0:
			yield [elems[0]]
			return
		for perm in self.make_perms(elems, r - 1):
			for i in range(r + 1):
				j = r - i
				yield perm[:j] + [elems[r]] + perm[j:]
		return

	# Make permuatations of size from
	def make_combs(self, size, l):
		if (size > l + 1):
			return
		if size == 0:
			yield []
			return
		if l == 0:
			for elem in self.elems[0]:
				yield [elem]
			return
		for c in self.make_combs(size, l - 1):
			yield c
		for elem in self.elems[l]:
			for c in self.make_combs(size - 1, l - 1):
				c.append(elem)
				yield c

	# Generate all P(n, r) permutations of r = size
	def generate(self, size):
		for comb in self.make_combs(size, len(self.elems) - 1):
			for perm in self.make_perms(comb, len(comb) - 1):
				yield perm
		return


COLOR_GREEN = "\033[0;32m"
COLOR_RED = "\033[1;31m"
COLOR_RESET = "\033[0;0m"

def verify_for_size(f, l, m, size, verbose = False):
	verifier = EmailVerifier()
	for template in email_templates[size]:
		user = template.format(f = f, l = l, m = m)
		if len(user) < 3:
			continue
		try_addr = EMAIL_FORMAT.format(user = user, domain = domain)
		if verbose:
			print("Checking `" + try_addr + "`...", end = '', flush = True)
		verif = verifier.verify(try_addr)
		if verif:
			print(COLOR_GREEN + "." + COLOR_RESET, end = '', flush = True)
			return try_addr
		else:
			print(COLOR_RED + "." + COLOR_RESET, end = '', flush = True)
			if verbose:
				print(" ")

	return None

# Sufficiently random email that nobody should
# actually have this as a valid one
RANDOM_EMAIL = "prhzdge.yrtheu"

# Find the email address, given the below parameters
# Permutates over the possible combinations of first and lastname
# including .(period), eg. first.last@ and then checks
# each email.
def find_email(first, middle, last, domain, args):
	if not EmailVerifier().check_domain(domain):
		raise ValueError("Invalid domain name for email server.")
	elif EmailVerifier().verify(EMAIL_FORMAT.format(user = RANDOM_EMAIL, domain = domain)):
		raise ValueError("Domain seems to accept all email addresses.")
	elif args.verbose:
		print("Domain checks successful")
	# Can use either from each of elems
	elems = [ (first, first[0]), (last, last[0]) ]
	if middle:
		elems.append((middle, middle[0]))

	email, email_list = None, []
	p_gen = Permutator(elems)

	# Order of lengths is 2, 3, 1
	# to match most common observations
	for leng in (2, 3, 1):
		for perm in p_gen.generate(leng):
			first = perm[0] 
			last = perm[1] if len(perm) > 1 else None
			middle = perm[2] if len(perm) > 2 else None
			email = verify_for_size(first, last, middle, leng, args.verbose)
			if email:
				email_list.append(email)
				if not args.find_all:
					return email_list

	# Not found, probably works for Amazon :D
	return email_list

# Automatically append .com if no tld is
# present in domain.
TLD = [".com", ".org", ".net"]
def correct_for_tld(domain):
	if domain == "":
		return domain
	domain_flag = False
	for tld in TLD:
		if domain.endswith(tld):
			domain_flag = True
			break

	if not domain_flag:
		return domain + TLD[0]
	else:
		return domain 


# Check internet connectivity, using Google
# the standard connection tester :)
google_url = "https://google.com/"
def check_connectivity():
	print("Checking connection...")
	try:
		request.urlopen(google_url)
		return True
	except urllib.error.URLError:
		return False

parser = argparse.ArgumentParser(
	description='Find email address given a name and a domain.')
parser.add_argument('--batch', dest='batch', default = False,
	action='store_true', help = "Batch mode, process multiple requests")
parser.add_argument('-v', dest='verbose', default = False, 
	action='store_true', help = "Verbose mode")
parser.add_argument('--all', dest='find_all', default = False, 
	action='store_true', help = "Find all possible addresses instead \
			of stopping at the first successful")

if __name__ == "__main__":
	if not check_connectivity():
		print("Can't connect to internet, exiting.")
		sys.exit(1)
	else:
		print("Connectivity okay.")

	args = parser.parse_args()
	loops = 1000 if args.batch else 1
	input_list = []
	for l in range(loops):
		name = input("Name({first} {last}): ")
		if name == "":
			break
		domain = correct_for_tld(input("Domain: "))
		input_list.append((domain, name.split()))

	prev_domain = ""
	for domain, name_parts in input_list:
		if len(name_parts) > 2:
			first, middle, last = name_parts[0], name_parts[1].lower(), name_parts[2]
		else:
			first, last = name_parts; middle = None

		if domain == "":
			domain = prev_domain

		try:
			email_list = find_email(first.lower(), middle, last.lower(), domain, args)
			print()
			if len(email_list) > 0:
				print("Valid Emails: ", email_list)
			else:
				print("Not Found")
			prev_domain = domain
		except ValueError as e:
			print("Error: " + str(e))
			sys.exit(1)

		# Successful return
		sys.exit(0)
		