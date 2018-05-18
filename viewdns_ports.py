import urllib

import requests

from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'name': 'ViewDNS Port Enumerator',
        'author': 'Jose Nazario',
        'description': 'Queries ViewDNS using the \'host\' operator to update the \'ports\' table.',
        'comments': (
            '',
        ),
        'required_keys': ('viewdns_key', ),
        'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL',
        'options': (
        ),
    }
    
    # http://viewdns.info/api/docs/port-scanner.php
    
    def module_run(self, hosts):
        key = self.get_key('viewdns_key')
        baseurl = 'https://api.viewdns.info/portscan/'
        for host in hosts:
            params = {'key': key,
                      'host': host,
                      'output': 'json'}
            params = urllib.urlencode(params)
            url = "%s%s?%s" % (base_url, params)
            resp = self.request(url)
            for info in resp.json['respose']['port']:
                if info['status'] != 'open':
                    continue
                self.add_ports(host=host, 
                               port=info['number'], 
                               protocol=info['service'].lower())
