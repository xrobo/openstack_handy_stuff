OPTIONS='-LLL -x'
EXTRA='ldif-wrap=no'
SEARCHBASE='OU=corp,DC=xrobo,DC=lab'
SCOPE='sub'
BINDDN='CN=benchmark,OU=corp,DC=xrobo,DC=lab'
PASSWORD='***'
LDAPHOST='ldaps.xrobo.lab'
LDAPURI="ldaps://${LDAPHOST}"
OUTFILE='outfile.txt'
ATTRIBUTES='DN'

# exactly as specified in Keycloak:
FILTER='(&(objectCategory=person)(objectclass=user)((memberOf:1.2.840.113556.1.4.1141:=CN=keycloak,OU=Groups,OU=corp,DC=xrobo,DC=lab))(!(userAccountControl:1.2.840.113056.1.4.803:=2)))'
# Fixed for "openldap-clients":
FILTER='(&(objectCategory=person)(objectclass=user)(memberOf:1.2.840.113556.1.4.1141:=CN=keycloak,OU=Groups,OU=corp,DC=xrobo,DC=lab)(!(userAccountControl:1.2.840.113056.1.4.803:=2)))'

function main() {
        ldapsearch \
                $OPTIONS \
                -o $EXTRA \
                -b "$SEARCHBASE" \
                -s $SCOPE \
                -D "$BINDDN" \
                -w "$PASSWORD" \
                -H $LDAPURI \
                "$FILTER" \
                $ATTRIBUTES | grep -v '^$' > $OUTFILE
}

time main
echo -n "Items: "; wc -l $OUTFILE
