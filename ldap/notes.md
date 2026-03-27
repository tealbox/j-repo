[LDAP Basic Terminology] What is a DC? What is an OU? What are Bind DN, Base DN, and Suffix? What is Anonymous Bind? ldapsearch Options

All elements that make up an LDAP tree are called objects . Organizational Units (OUs) and users are both objects . These objects have a name that uniquely identifies them in the tree. This is called a Distinguish Name (DN).

The notation is as follows: "[Attribute 1]=[Attribute Value],[Attribute 2]=[Attribute Value],,,,[Attribute 3]=[Attribute Value]". For example, the top of a tree is always a 'domain name' , and the DN of this domain name  is written as "dc=example,dc=com".

Here, we encounter the attribute called DC (Domain Component) , which is a component of a domain name. In this example, there are two DCs, but there is no limit to the number, and the number is not significant . One DC is sufficient. However, similar to OIDs (although duplication has no impact as they rarely interact), the principle is that "domain names should not overlap with those of other companies," so it is common to use the domain name held by that company's DNS.

An OU (Organization Unit) is like a folder in a file system; it's an object that stores users. If users are like leaves in a tree, then OUs are like branches in the tree.

What are LDAP bind DN and base DN?
Binding means logging into an LDAP service . Once bound , you can use the LDAP service (for searching, verifying authentication information for other users, etc.)
Therefore , the Bind DN is the user used when logging into the LDAP service .

The base DN indicates which OU (Organizational Unit) information you will be working with after logging into the LDAP service. This is also known as the suffix.

Let's look at a concrete example. On the LDAP client, execute the ldapsearch command as follows:
[root@localhost ~]# **ldapsearch -h 192.168.1.1 -x -D "cn=Manager,dc=example,dc=com" -W -b "ou=eigyo,dc=example,dc=com" cn=test* **

Then, the PC that executed this command binds (logs in) to the LDAP server at 192.168.1.1 with the user "cn=Manager,dc=example,dc=com", and searches for users under "ou=eigyo,dc=example,dc=com" whose cn starts with "test".

In this case, the bind DN will be "cn=Manager,dc=example,dc=com" and the base DN will be "ou=eigyo,dc=example,dc=com" .

ldapsearch options
-h: Option to specify the IP address or FQDN of the LDAP server.
-x: Option to use simplified authentication instead of SASL
-D: Option to specify the bind DN
-W: An option that prompts for a bind password for the bind DN specified with -D after pressing Enter.
-b: Option to specify the base DN


What is an anonymous bind?
Normally, a specific DN (username) is required for binding, but it's possible to use the LDAP service without a bind DN . This is called anonymous binding .

For example, with the ldapsearch command, if you don't specify -D, it will be an anonymous bind.

However, allowing anonymous use of all LDAP services poses a security risk , so we limit the scope of services that can be used by specifying ACLs in slapd.conf .

For example, if you write an ACL like the one below, anonymous binding will only allow you to view the mail attribute values of users within the range "ou=1g,ou=eigyo,dc=example,dc=com". (cn=Manager is configured to allow writing as well.)

access to dn.subtree="ou=1g,ou=eigyo,dc=example,dc=com" attrs=mail 
by "cn=Manager,dc=example,dc=com" write 
by anonymous read
