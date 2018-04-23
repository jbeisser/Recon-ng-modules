from recon.core.module import BaseModule
import requests

class Module(BaseModule):
    meta = {
        'name': 'Graynoise IP Lookups',
        'author': 'Jose Nazario',
        'description': 'Uses Graynoise to update the \'domains\' table.',
        'comments': (
            '',
        ),
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
    }

    def module_run(self, hosts):
        for ip_address in hosts:
            self.heading(ip_address, 1)
            resp = requests.post('http://api.greynoise.io:8888/v1/query/ip', data = {'ip':ip_address})
            if resp.json()['status'] == 'unknown' or resp.status_code != 200:
                continue
            try: domains = { x['rdns_parent'] for x in resp.json()['records'] if len(x['rdns_parent']) > 0 }
            except KeyError: continue
            self.add_domains(domains)
