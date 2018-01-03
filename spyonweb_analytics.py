from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        'name': 'SpyOnWeb analyzer using Google Analytics identifier',
        'author': 'jose nazario',
        'description': 'Parses the SpyOnWeb data for shared Google Analytics IDs, looking for other domains that share the Google Analytics identifier. Updates the \'domains\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }
    
    def module_run(self, domains):
        api_secret = self.get_key('spyonweb_secret')
        summary_url = 'https://api.spyonweb.com/v1/summary/{}?access_token={}'
        analytics_url = 'https://api.spyonweb.com/v1/analytics/{}?access_token={}'
        for domain in domains:
            self.heading(domain, 0)
            domainresp = self.request(summary_url.format(domain, api_secret))
            if domainresp.json['status'] != 'found':
                continue
            analytics = domainresp.json['result']['summary'][domain]['items'].get('analytics', {})
            for aid in analytics.keys():
                resp = self.request(analytics_url.format(aid, api_secret))
                for k,data in resp.json['result']['analytics'].iteritems():
                    self.heading(k, 1)
                    for new_domain,date in data['items'].iteritems():
                        self.add_domains(new_domain)
