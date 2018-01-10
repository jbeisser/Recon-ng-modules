from recon.core.module import BaseModule

class Module(BaseModule):

    meta = {
        'name': 'DNSTrails data miner',
        'author': 'jose nazario @jnazario',
        'description': 'Retrieves hosts sharing the same IP from the DNSTrails data set. Updates the \'hosts\' table.',
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
    }
    
    def _fmt_hostname(self, host, domain):
        if host is not none:
            return '{}.{}'.format(host, domain)
        else:
            return domain


    def module_run(self, ips):
        for ip in ips:
            self.heading(ip, level=0)
            url = 'https://app.securitytrails.com/api/search/by_type/ip/{}'.format(ip)
            resp = self.request(url)
            if resp.status_code == 200:
                hosts = map(lambda x: self._fmt_hostname(x['host'], x['domain']), resp.json['result']['items'])
                for host in hosts:
                    self.add_hosts(host=host, ip_address=ip) 
