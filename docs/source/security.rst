.. _stream:

Security
==========

Given the importance of IT security in a corporate environment, the entire stack used to run Kavalan is configured/designed to prevent
unauthorized access. The following sections deal with each level of the stack and discuss the security mechanisms implemented.

Server and Firewall
-----------------------

At Wu-Fu Laboratories, the Kavalan Managment System runs on CentOS 6.0 with default settings for SELinux (enforcing). Iptables is configured
as follows::

    :INPUT DROP [0:0]
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [1863:1287415]
    -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
    -A INPUT -p icmp -m icmp --icmp-type 8 -j DROP
    -A INPUT -p icmp -m icmp --icmp-type 8 -j REJECT --reject-with icmp-host-prohibited
    -A INPUT -p icmp -j ACCEPT
    -A INPUT -i lo -j ACCEPT
    -A INPUT -s 192.168.2.0/24 -p tcp -m state --state NEW -m tcp --dport 443 -j ACCEPT
    -A INPUT -p tcp -m state --state NEW -m tcp --dport 21 -j ACCEPT
    -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
    -A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
    -A INPUT -j REJECT --reject-with icmp-host-prohibited
    -A FORWARD -j REJECT --reject-with icmp-host-prohibited


Only computers in the local area network is permitted to access Kavalan.

Database
----------

Kavalan currently runs on MySQL 5.1.52-1 at Wu-Fu Laboratories. It uses an isolated database; the database user that Django uses
to access this database is grant permissions ONLY on this database; the root user's login credential is NOT available to the web server.


Web Server
-------------

Kavalan runs on a Nginx + Apache setup, with Nginx serveing as the reverse proxy and Apache binding to the localhost only.
ALL traffic to/from the server is transmitted over HTTPS.

Kavalan Management System/Django
-------------------------------------

Kavalan requires the user to be authenticated before any action that accesses the database will be permitted. It uses the default
Django authentication backend, which stores the user passwords in salted-hashes. As mentioned above, all traffic to/from the server
is encrypted, preventing man-in-the-middle attack.

Document Access Security
***************************

For information on the security mechanisms specific to Doc Engine, please refer to :ref:`doc-engine-security`.


