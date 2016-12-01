# ssl-certificate-enumerator
A script to perform SSL certificate enumeration

## Usage

```
python ssl_certificate_enumerator.py --help
usage: ssl_certificate_enumerator.py [-h] [-f INPUTFILE] [-d DELIMITER]
                                     [-o OUTPUTFILE] [-t TARGET] [-p PORT]
                                     [-i] [-u] [-x] [-b] [-e] [-n] [-s] [-v]
                                     [-z]

SSL Certificate Enumerator

optional arguments:
  -h, --help            show this help message and exit
  -f INPUTFILE, --inputfile INPUTFILE
                        Input file with IP and Port to check
  -d DELIMITER, --delimiter DELIMITER
                        Input file field delimiter
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Output file to save
  -t TARGET, --target TARGET
                        Target host or IP address
  -p PORT, --port PORT  Target port
  -i, --issuer          Show SSL certificate issuer
  -u, --issuedto        Show SSL certicate issued to
  -x, --expireon        Show SSL certicate expiry date
  -b, --validfrom       Show SSL certicate validty from
  -e, --expired         Show SSL certicate is expired or not
  -n, --serialno        Show SSL certicate serial number
  -s, --signalgo        Show SSL certicate signature algorithm
  -v, --certver         Show SSL certicate version
  -z, --tls12method     Use TLS1_2_METHOD
```

## Requirements

Please ensure you have the following python packages installed: OpenSSL, py509, argparse

How to install:

pip install package_name

easy_install package_name
