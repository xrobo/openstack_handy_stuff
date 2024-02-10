OPTS='--endpoint http://localhost:2379'
ROOT=/root
TMPF=/tmp/$$.tmp

etcdctl $OPTS ls -r $ROOT > $TMPF

for key in $(< $TMPF); do
    if val=$(etcdctl $OPTS get $key 2>/dev/null); then
        echo "$key: $val"
    fi
done

rm -f $TMPF
