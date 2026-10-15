1) create CSR and then self sign,
2) direct self  sign using SAN with IP and DNS

san.cnf file is saved with the req_extensions and x509_extensions directives pointing to your custom [ v3_req ] block, 
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
ST = California
L  = San Francisco
O  = My Company Ltd
OU = IT Department
CN = 192.168.1.50

[ v3_req ]
basicConstraints     = CA:FALSE
keyUsage             = digitalSignature, keyEncipherment
extendedKeyUsage     = serverAuth, clientAuth
subjectAltName       = @alt_names

[ alt_names ]
IP.1 = 192.168.1.50
IP.2 = 10.0.0.15
DNS.1 = example.local
DNS.2 = www.example.local

```


**Workflow 1: Create a CSR, then Self-Sign it**

Use this method if you want to practice the standard, multi-step Certificate Authority (CA) process. You will first create a private key and a Certificate Signing Request (CSR), then act as your own CA to sign it.
**Step 1: Generate the Private Key and CSR**
openssl req -new -nodes -keyout server.key -out server.csr -config san.cnf
(OpenSSL automatically reads req_extensions from the config file and bundles the SAN IP/DNS details directly inside the server.csr file).

**Verification Command for CSR**
openssl req -in server.csr -noout -text | grep DNS

**Step 2: Sign the CSR using its own Private Key**
server.key is created in step 1
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt -extfile san.cnf -extensions v3_req
• Note: When using openssl x509 -req, OpenSSL strips extensions out of the raw CSR by default due to safety regulations. You must explicitly add -extfile san.cnf -extensions v3_req here to push the SAN details back into the final server.crt file.



**Workflow 2: Direct Self-Sign (Single Step)**

Use this method to generate your private key and finished self-signed certificate immediately, bypassing the CSR phase entirely.
**Step 1: Generate Key and Certificate together**
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -config san.cnf

• Note: Because the file contains x509_extensions = v3_req, OpenSSL automatically binds your SAN block to the certificate without forcing you to append terminal flags.

**Verification Command (Works for Both)**

To ensure your IP addresses and DNS domains made it into the final certificate file, run:
openssl x509 -in server.crt -text -noout | grep -A 2 "Subject Alternative Name"


==============================================================

Workflow 1 into a professional setup. Instead of having the certificate sign itself, you will create a distinct Root CA (Certificate Authority) and use it to sign your server certificate.
This is the standard approach used in corporate networks. By installing this custom Root CA on your devices, every certificate it signs will be instantly trusted by your browsers and operating systems.
You can use the exact same san.cnf file from the previous step.

Step 1: Create the Root CA Key Pair

First, you need to create the Root CA's private key and its self-signed "Root Certificate." This is the master identity that will act as your mini Certificate Authority.
1. Generate the Root CA Private Key:
bash
openssl genrsa -out rootCA.key 4096
Use code with caution.
2. Generate the Root CA Certificate (valid for 10 years):
bash
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 \
  -out rootCA.crt \
  -subj "/C=US/ST=California/L=San Francisco/O=My Company Ltd/CN=My Private Root CA"
Use code with caution.

Step 2: Generate the Server Key and CSR

Next, generate the server's private key and Certificate Signing Request (CSR) exactly as you did before.
bash
openssl req -new -nodes \
  -keyout server.key \
  -out server.csr \
  -config san.cnf
Use code with caution.
(OpenSSL bundles your IP addresses and DNS domains from san.cnf into the server.csr file).

Step 3: Sign the Server CSR with your Root CA

Now, act as the CA. Take the server.csr, apply your rootCA.key and rootCA.crt, and enforce the SAN extensions block from your configuration file.
bash
openssl x509 -req -days 365 \
  -in server.csr \
  -CA rootCA.crt \
  -CAkey rootCA.key \
  -CAcreateserial \
  -out server.crt \
  -extfile san.cnf \
  -extensions v3_req \
  -sha256
Use code with caution.

What just happened?

• You used -CA and -CAkey to sign the certificate with your new Root CA instead of the server's own key.
• -CAcreateserial creates a tracking file (rootCA.srl) to manage unique certificate serial numbers.
• -extfile san.cnf -extensions v3_req explicitly forces your IP and DNS entries into the final server.crt.

Step 4: Verify the Trust Chain

You can verify that the new certificate was successfully signed by your Root CA and retains your SAN IPs with these two commands:
1. Check the SAN contents:
bash
openssl x509 -in server.crt -text -noout | grep -A 2 "Subject Alternative Name"
Use code with caution.
2. Verify the certificate against the Root CA:
bash
openssl verify -CAfile rootCA.crt server.crt
Use code with caution.
(Expected Output: server.crt: OK)
