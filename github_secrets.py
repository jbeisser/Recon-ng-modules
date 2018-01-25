from recon.core.module import BaseModule
import os

class Module(BaseModule):
    meta = {
        'name': 'Github Code Analyzer',
        'author': 'j nazario (@jnazario)',
        'description': 'Uses the Github API to search for possible vulnerabilites in source code by leveraging Github Dorks and the \'domains\' search operator. Updates the \'vulnerabilities\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',

    }

    # via https://www.hackerone.com/blog/how-to-recon-and-content-discovery
    def module_run(self, domains):
        dorks = ('secret_key', 'API_key', 'aws_key', 'aws_secret', 'password', 'FTP', 'login', 'github_token')
        for domain in domains:
            self.heading(domain, level=0)
            for dork in dorks:
                query = '%s %s' % (domain, dork)
                for result in self.search_github_api(query):
                    data = {
                        'reference': query,
                        'example': result['html_url'],
                        'category': 'Github Dork',
                    }
                    for key in sorted(data.keys()):
                        self.output('%s: %s' % (key.title(), data[key]))
                    print(self.ruler*50)
                    self.add_vulnerabilities(**data)    
