from recon.core.module import BaseModule

import dns.resolver

class Module(BaseModule):
    meta = {
        'name': 'DNS SOA record enumerator',
        'author': 'Jose Nazario',
        'description': 'Uses DNS SOA records to update the \'contacts\' table.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        for domain in { x.lower() for x in domains }:
            try:
                ans = dns.resolver.query(domain, 'SOA')
            except (dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.NXDOMAIN):
                continue
            for a in ans.rrset.items:
                e = a.to_text().split()[1].replace('.', '@', 1).rstrip('.')
                self.add_contacts(email=e)
