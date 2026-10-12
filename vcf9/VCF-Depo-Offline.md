# **Offline Depot**

**https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/binary-management-for-vmware-cloud-foundation/set-up-an-offline-depot-web-server-for-vmware-cloud-foundation.html**


<img width="588" height="501" alt="image" src="https://github.com/user-attachments/assets/550275ad-b4d2-4a03-8d1a-43edce9bb47b" />



```
cat << 'EOF' > /root/http-certificates/conf.cfg
[req]
distinguished_name = req_distinguished_name
req_extensions = req_ext
prompt = no

[req_distinguished_name]
C = SE 
ST = Stockholm
L = Stockholm
O = Rainpole
OU = IT
CN = depot.rainpole.io

[req_ext]
subjectAltName = @alt_names

[alt_names]
IP.1 = 172.16.10.11
DNS.1 = depot.rainpole.io
EOF
```

Add the VMSA public key to the certificate:
cat /var/lib/vmware/vmca/root.cer >> server.crt


```
Install Apache HTTP Server, update the operating system, and reboot the VM.
tdnf install httpd tar jq --assumeyes
tdnf update --assumeyes
reboot
```

```
mkdir -p /var/www/html
mkfs.ext4 /dev/sdb
echo "/dev/sdb /var/www/html ext4 defaults 0 2" >> /etc/fstab
mount -a

```
```
mkdir /root/http-certificates
openssl genpkey -out /root/http-certificates/server.key -algorithm RSA -pkeyopt rsa_keygen_bits:2048
```

Create a .csr file by using the .key and .cfg files.

**openssl req -new -key /root/http-certificates/server.key -out /root/http-certificates/request.csr -config conf.cfg**

**VMware Certificate Authority (VMCA)**

Transfer request.csr to the vCenter (for example, to /root/).
SSH into vCenter as root and run the following commands:
openssl x509 -req -days 365 -in **/root/request.csr** -CA /var/lib/vmware/vmca/root.cer -CAkey /var/lib/vmware/vmca/privatekey.pem -CAcreateserial -out /root/server.crt -sha256 -extensions req_ext -extfile conf.cfg
**Add the VMSA public key to the certificate:**
cat /var/lib/vmware/vmca/root.cer >> /root/server.crt


Copy server.crt to /root/http-certificates/.
Clean the .crt certificate files.
rm -f /root/server.crt /root/request.csr


enable SSL modules and replace the operations@rainpole.io and depot.rainpole.io:443 example values with your own.
edit the /etc/httpd/conf/httpd.conf and /etc/httpd/conf/extra/httpd-ssl.conf files.
```
sed -i 's|#LoadModule ssl_module|LoadModule ssl_module|' /etc/httpd/conf/httpd.conf

sed -i 's|#LoadModule socache_shmcb_module|LoadModule socache_shmcb_module|' /etc/httpd/conf/httpd.conf

sed -i 's|#Include conf/extra/httpd-ssl.conf|Include conf/extra/httpd-ssl.conf|' /etc/httpd/conf/httpd.conf

sed -i 's|DocumentRoot "/etc/httpd/html"|DocumentRoot "/var/www/html"|' /etc/httpd/conf/httpd.conf

sed -i 's|<Directory "/etc/httpd/html"|<Directory "/var/www/html"|' /etc/httpd/conf/httpd.conf

sed -i 's|DocumentRoot "/etc/httpd/html"|DocumentRoot "/var/www/html"|' /etc/httpd/conf/extra/httpd-ssl.conf

sed -i 's|ServerAdmin you@example.com|ServerAdmin operations@rainpole.io|' /etc/httpd/conf/extra/httpd-ssl.conf

sed -i 's|ServerName www.example.com:443|ServerName depot.rainpole.io:443|' /etc/httpd/conf/extra/httpd-ssl.conf
```

In the **/etc/httpd/conf/httpd.conf** file, locate the DocumentRoot "/var/www/html" section and change **Required all denied** to **Required all granted**
In the /etc/httpd/conf/extra/httpd-ssl.conf file, **locate the </VirtualHost> tag and above the tag, paste the following configuration code.**
```
<Directory /var/www/html/PROD/COMP>
        AuthType Basic
        AuthName "Basic Authentication"
        AuthUserFile /etc/httpd/conf/.htpasswd
        require valid-user
</Directory>
<Directory /var/www/html/PROD/metadata>
        AuthType Basic
    AuthName "Basic Authentication"
    AuthUserFile /etc/httpd/conf/.htpasswd
    require valid-user
</Directory>
<Directory "/var/www/html/PROD/COMP/Compatibility/VxrailCompatibilityData.json">
        # VxRail VVS Cookie Validation (VCF 5.0)
        <If "%{HTTP:Cookie} == 'ngssosession=ngsso-token' ">
        Require all granted
        </If>
</Directory>
<Directory /var/www/html/PROD/vsan/hcl>
        Require all granted
</Directory>
        # Those Alias statements are needed only for VCF 5.1.0.0.
        Alias /products/v1/bundles/lastupdatedtime /var/www/html/PROD/vsan/hcl/lastupdatedtime.json
        Alias /products/v1/bundles/all /var/www/html/PROD/vsan/hcl/all.json
        # Needed only if UMDS downloads are presented
<Directory /var/www/html/umds-patch-store>
        Require all granted
</Directory>
```

```
htpasswd -c /etc/httpd/conf/.htpasswd Username
chown apache /etc/httpd/conf/.htpasswd
chmod 0400 /etc/httpd/conf/.htpasswd
httpd -t
systemctl start httpd
systemctl status httpd
systemctl enable httpd

Remove the default Apache index file.
rm -f /var/www/html/index.html


chown apache -R /var/www/html/
find /var/www/html -type d -exec chmod 0500 {} \;
find /var/www/html -type f -exec chmod 0400 {} \;
chmod 755 /var/www/
chmod 755 /var/www/html/
```


Enable HTTPS in the Apache Server - In the “/etc/httpd/conf/httpd.conf” file, remove the “#” symbol in front of the following lines:
“#LoadModule ssl_module /usr/lib/httpd/modules/mod_ssl.so”
“#LoadModule socache_shmcb_module /usr/lib/httpd/modules/mod_socache_shmcb.so”
“#Include conf/extra/httpd-ssl.conf”

You could use the following commands to do the necessary changes in an automatic way:
sed --in-place 's|#LoadModule ssl_module|LoadModule ssl_module|' /etc/httpd/conf/httpd.conf
sed --in-place 's|#LoadModule socache_shmcb_module|LoadModule socache_shmcb_module|' /etc/httpd/conf/httpd.conf
sed --in-place 's|#Include conf/extra/httpd-ssl.conf|Include conf/extra/httpd-ssl.conf|' /etc/httpd/conf/httpd.conf


**https://knowledge.broadcom.com/external/article/312168/vcf-offline-depot-deployment.html**
**https://knowledge.broadcom.com/external/article/450638/vcf-offline-depot-connectivity-fails-due.html**
**https://blog.philbendeck.com/VCF/VCF9-Offline-Depot**
**https://www.vmtechnics.com/2025/10/15/setting-up-an-offline-depot-for-vmware-cloud-foundation-9-x-using-apache-on-ubuntu/**

## Public URLs Required for Online Functionalities for VCF and vSphere Foundation
https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/planning-and-preparation/public-urls-required-for-vmware-cloud-foundation.html
