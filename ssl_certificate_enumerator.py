#!/usr/bin/python
try:
	import OpenSSL 
	import py509
	import argparse
	import sys
	from py509 import client
	from datetime import datetime
except:
	print "Error: Missing python packages\n"
	print "Please ensure you have the following python packages installed:\n OpenSSL, py509, argparse\n"
	print "How to install:\npip install <package_name>\neasy_install <package_name>\n"
	sys.exit(0)

def get_host_certificate_tls1_2(host, port=443):
	import socket
	from OpenSSL import SSL
	import certifi
	ip_addr = socket.gethostbyname(host)
	sock = socket.socket()
	context = SSL.Context(SSL.TLSv1_2_METHOD)
	#context.set_options(SSL.OP_NO_SSLv2)
	context.load_verify_locations(certifi.where(), None)
	ssl_sock = SSL.Connection(context, sock)
	ssl_sock.connect((ip_addr, port))
	ssl_sock.do_handshake()
	return ssl_sock.get_peer_certificate()

#Description of script
parser = argparse.ArgumentParser(description="SSL Certificate Enumerator")

#Script command line options
parser.add_argument('-f', '--inputfile', help='Input file with IP and Port to check')
parser.add_argument('-d', '--delimiter', help='Input file field delimiter', type=str, default=",")
parser.add_argument('-o', '--outputfile', help='Output file to save')
parser.add_argument('-t', '--target', help='Target host or IP address')
parser.add_argument('-p', '--port', help='Target port', type=int, default=443)
parser.add_argument('-i', '--issuer', help='Show SSL certificate issuer', action='store_true')
parser.add_argument('-u', '--issuedto', help='Show SSL certicate issued to', action='store_true')
parser.add_argument('-x', '--expireon', help='Show SSL certicate expiry date', action='store_true')
parser.add_argument('-b', '--validfrom', help='Show SSL certicate validty from', action='store_true')
parser.add_argument('-e', '--expired', help='Show SSL certicate is expired or not', action='store_true')
parser.add_argument('-n', '--serialno', help='Show SSL certicate serial number', action='store_true')
parser.add_argument('-s', '--signalgo', help='Show SSL certicate signature algorithm', action='store_true')
parser.add_argument('-v', '--certver', help='Show SSL certicate version', action='store_true')
#parser.add_argument('-k', '--publickey', help='Show SSL certicate public key', action='store_true')
parser.add_argument('-z', '--tls12method', help='Use TLS1_2_METHOD', action='store_true')

args = parser.parse_args()

#Read input file
if args.inputfile:
	input_file = args.inputfile.encode('utf-8')
	input_file_delimiter = args.delimiter.encode('utf-8')
	f = None
	data = None
	#Read input file
	try:
		f = open(input_file, 'r')
		data = f.readlines()
		f.close()
	except:
		print "[!] Error: Input target file '%s' not found" % (input_file)
		sys.exit(1)
	if args.outputfile:
		output_file = args.outputfile.encode('utf-8')
		f = open(output_file, 'w')
		output_file_head = "Target Host,Target Port,"
		if args.issuer:
			output_file_head += "Issued By,"
		if args.issuedto:
			output_file_head += "Issued To,"
		if args.validfrom:
			output_file_head += "Valid From,"
		if args.expireon:
			output_file_head += "Expires On,"
		if args.expired:
			output_file_head += "Expired,"
		if args.serialno:
			output_file_head += "Serial Number,"
		if args.signalgo:
			output_file_head += "Signature Algorithm,"
		if args.certver:
			output_file_head += "Certificate Version,"
		output_file_head = output_file_head[:-1] + "\n"
		f.write(output_file_head)
		f.close()
	#Start reading lines from input file
	for line in data:
		line = (line.replace("\n","")).replace("\r","")
		#Read target IP Address
		target_ip = line.split(input_file_delimiter)[0]
		#Read target port
		target_port = line.split(input_file_delimiter)[1]
		certicate_info = None
		try:
			if not tls_1_2_method:
				certicate_info = client.get_host_certificate(target_ip, target_port)
			else:
				certicate_info = get_host_certificate_tls1_2(target_ip, target_port)
		except:
			print "[!] Error: Could not connect to %s:%s" % (target_ip, target_port)
			break;
		#Start enumerating SSL certificate
		ssl_cert_data = ""
		ssl_cert_data += ( target_ip + "," + target_port + "," )
		if args.issuer:
			ssl_cert_data += certicate_info.get_issuer().CN + ","
		if args.issuedto:
			ssl_cert_data += certicate_info.get_subject().CN + ","
		if args.validfrom:
			ssl_cert_data += str(datetime.strptime(certicate_info.get_notBefore(), "%Y%m%d%H%M%SZ")) + ","
		if args.expireon:
			ssl_cert_data += str(datetime.strptime(certicate_info.get_notAfter(), "%Y%m%d%H%M%SZ")) + ","
		if args.expired:
			if certicate_info.has_expired():
				ssl_cert_data += "Yes,"
			else:
				ssl_cert_data += "No,"
		if args.serialno:
			ssl_cert_data += str(certicate_info.get_serial_number()) + ","
		if args.signalgo:
			ssl_cert_data += certicate_info.get_signature_algorithm() + ","
		if args.certver:
			ssl_cert_data += str(certicate_info.get_version()) + ","
		ssl_cert_data = ssl_cert_data[:-1]
		print ssl_cert_data
		#Add a new line
		ssl_cert_data += "\n"
		#Save output file if command line option was set
		if args.outputfile:
			if len(ssl_cert_data)>0:
				f = open(output_file, 'a')
				f.write(ssl_cert_data)
				f.close()

#Target IP and Port	
if args.target and args.port:
	target_ip = args.target.encode('utf-8')
	target_port = args.port
	tls_1_2_method = args.tls12method
	certicate_info = None
	try:
		if not tls_1_2_method:
			certicate_info = client.get_host_certificate(target_ip, target_port)
		else:
			certicate_info = get_host_certificate_tls1_2(target_ip, target_port)
	except:
		print "[!] Error: Could not connect to %s:%s" % (target_ip, target_port)
		sys.exit(1)
	#Get information from SSL Certificate
	print "Target Host: %s" % (target_ip)
	print "Target Port: %s" % (target_port)
	print "Issued By: %s" % (certicate_info.get_issuer().CN)
	print "Issued To: %s" % (certicate_info.get_subject().CN)
	print "Valid From: %s" % (datetime.strptime(certicate_info.get_notBefore(), "%Y%m%d%H%M%SZ"))
	print "Validity Expiry: %s" % (datetime.strptime(certicate_info.get_notAfter(), "%Y%m%d%H%M%SZ"))
	if certicate_info.has_expired():
		print "Certificate Expired: Yes"
	else:
		print "Certificate Expired: No"
	print "Certificate Serial Number: %d" % (certicate_info.get_serial_number())
	print "Signature Algorithm: %s" % (certicate_info.get_signature_algorithm())
	print "Certificate Version: %d" % (certicate_info.get_version())
	#print "Public Key: %s" % ((certicate_info.get_pubkey()).type())
	#print ": %s" % (certicate_info.)
