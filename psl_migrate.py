from publicsuffix import fetch, PublicSuffixList

from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'name': 'Public Suffix List migrator',
        'author': 'Jose Nazario @jnazario',
        'description': 'Uses the PSL to update the \'domains\' table from all hostnames.',
        'comments': (
            'This module uses the PSL to find domains from hostnamnes',
        ),
        'required_keys': ['whoxy_key'],
        'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL'
    }
    
    def module_run(self, hosts):
        psl_file = fetch()
        psl = PublicSuffixList(psl_file)
        
        seen = set()
        for host in hosts:
            domain = psl.get_public_suffix(host)
            if domain in seen:
                continue
            else:
                self.add_domains(domain)
                seen.add(domain)
