import conf_prod as conf
import cred_prod as cred
# import conf as conf
# import cred as cred
import re
from keystoneauth1 import identity
from keystoneauth1 import session
from octaviaclient.api.v2.octavia import OctaviaAPI as o_client
from heatclient.client import Client as h_client

from keystoneclient.client import Client as k_client

auth = identity.Password(auth_url = conf.os['auth_url'],
					username = cred.os['username'],
					password = cred.os['password'],
					project_id = cred.os['project_id'],
					user_domain_id = cred.os['user_domain_name'])
sess = session.Session(auth=auth, verify=False)

octavia = o_client(session=sess, endpoint=conf.os['octavia_endpoint'])
heat    = h_client(session=sess, version=1)
keystone= k_client(session=sess)

def cluster_uuids():
    uuid_list = []
    for stack in heat.stacks.list():
        params = heat.stacks.get(stack.id).parameters
        if "cluster_uuid" in params:
            uuid_list.append(params["cluster_uuid"])
    return uuid_list

def rm_lbs(lbs, cluster_uuids):
    for lb in lbs["loadbalancers"]:
        lb_re = re.search("^kube_service_([\da-f]{8}(-[\da-f]{4}){3}-[\da-f]{12})", lb["name"])
        if lb_re and lb_re.group(1) not in cluster_uuids:
            print("Removing " + 
                lb["project_id"] + '/' + keystone.projects.get(lb["project_id"]).name +
                ' ' + lb["id"] + '/' + lb["name"])
            # octavia.load_balancer_delete(lb_id=lb["id"], cascade=True)
        else: print("Skipping " + 
                lb["project_id"] + '/' + keystone.projects.get(lb["project_id"]).name +
                ' ' + lb["id"] + '/' + lb["name"])

rm_lbs(octavia.load_balancer_list(limit=4), cluster_uuids())
