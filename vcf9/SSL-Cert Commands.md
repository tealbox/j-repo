```
[ req ]
default_bits        = 2048
default_md          = sha256
distinguished_name  = req_distinguished_name
req_extensions      = v3_req
x509_extensions     = v3_req
prompt              = no

[ req_distinguished_name ]
C  = US
ST = Texas
L  = Frisco
O  = VCF LAB CAS
OU = IT Department
CN = vcfstore8820.vcflab.net

[ v3_req ]
basicConstraints     = CA:FALSE
keyUsage             = digitalSignature, keyEncipherment
extendedKeyUsage     = serverAuth, clientAuth
subjectAltName       = @alt_names

[ alt_names ]
# --- IP Addresses ---
IP.1 = 192.168.1.50
IP.2 = 10.0.0.15
IP.3 = 127.0.0.1

# --- DNS Domains ---
DNS.1 = vcflab.net
DNS.2 = www.vcflab.net
DNS.3 = api.vcflab.net
```

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -config san.cnf

openssl x509 -in server.crt -text -noout | grep -A 2 "Subject Alternative Name"

To check in CSR:
openssl req -in request.csr -noout -text | grep DNS


provided, the -extensions v3_req flag was omitted because of a specific automation trick added to the san.cnf file: x509_extensions = v3_req.
By including that single line inside the configuration file, you completely eliminate the need to type out -extensions v3_req on your command line.


How it works behind the scenes

When you run openssl req -x509, OpenSSL reads the [ req ] block inside your configuration file. Because the file contains both pointers, it acts as an automatic override:
1. req_extensions = v3_req: This tells OpenSSL to look at v3_req if you are generating a CSR (Certificate Signing Request).
2. x509_extensions = v3_req: This tells OpenSSL to look at v3_req if you are using the -x509 flag to generate a Self-Signed Certificate.
Because x509_extensions is hardcoded right into the [ req ] block of the configuration file, OpenSSL automatically loads your IP addresses and DNS records without making you type the extra command-line flag.



What if you prefer to use the flag?

If you remove the x509_extensions = v3_req line from the file, then you must bring back the flag on your command line, like this:
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -config san.cnf \
  -extensions v3_req




