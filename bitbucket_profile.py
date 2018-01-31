from recon.core.module import BaseModule
from urllib import quote_plus
from urlparse import urlparse

class Module(BaseModule):
    meta = {
        'name': 'Bitbucket Profile Enumerator',
        'author': 'j nazario (jnazario)',
        'description': 'Uses the Bitbucket API to enumerate users and discover their websites. Updates the \'profile\' table with the results.',
        'query': "SELECT DISTINCT username FROM profiles WHERE username IS NOT NULL AND resource LIKE 'Bitbucket'",
    }
    
    def module_run(self, users):
        for user in users:
            self.heading(user, level=0)
            resp = self.request('https://bitbucket.org/api/2.0/users/{}'.format(user))
            if resp.status_code == 200:
                url = resp.json.get('website', '')
                if not urlparse(url).netloc.lower().endswith('bitbucket.org'):
                    # avoid self
                    self.add_profiles(username=user, url=url, resource='website', category='personal')
