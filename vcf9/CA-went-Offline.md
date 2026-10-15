what will happened if CA root server is not reachable on network?

Nothing will happen to your TLS/SSL handshake, and your connections will continue to work perfectly.
A Root CA (Certificate Authority) certificate is implicitly trusted because it is installed directly on your local device's operating system or browser trust store. When a client (like a web browser) connects to your server, it evaluates the trust chain completely offline.
Here is exactly how this works and what actually happens behind the scenes:

1. Trust Verification is Entirely Offline

When your browser connects to https://192.168.1.50, the server hands over server.crt.
• The browser extracts the signature on server.crt.
• It looks inside its own local memory for the matching rootCA.crt that you installed earlier.
• It uses mathematical cryptography to verify that the signature matches the local Root CA key.
• Zero network traffic is sent to the Root CA server during this cryptographic math check.

2. The Real Risk: Revocation Checks (CRL and OCSP)

The only time a browser ever tries to reach out to a CA over the network during a connection is to check if a certificate has been revoked (canceled early due to a leak or breach). It does this using two protocols:
• CRL (Certificate Revocation List) – A file downloaded from the CA listing bad certificates.
• OCSP (Online Certificate Status Protocol) – A live query sent to the CA asking "is this specific certificate still good?"
Because you generated a simple private Root CA using standard OpenSSL commands, your certificate does not contain CRL or OCSP network pointers (URIs). Therefore, your browser won't even attempt to contact a network server; it will instantly assume the certificate is valid.

What if you did add CRL/OCSP links and the CA server went down?

If you advanced your setup to include these features and the CA server became unreachable:
• Most modern browsers (Chrome, Edge, Safari): They operate on a "soft-fail" policy. If they cannot reach the CA's revocation server, they skip the check and let the connection go through anyway to prevent breaking the local network.
• Firefox: It can be configured for "hard-fail", which means it might show an error if it absolutely cannot verify the revocation status.

Summary

Your Root CA server can be completely powered off, destroyed, or disconnected from the network, and your server certificate will still be 100% trusted and functional. You only need the Root CA files active on your administrator machine when you want to sign a new certificate.

