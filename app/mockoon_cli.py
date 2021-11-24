import subprocess
import json
import config
import yaml

class MockoonCLI(object):
    def __init__(self):
        self.t_url = config.TRAEFIK_URL
        self.m_cli = config.MOCKOON_CLI

    def get_data_from_cli(self):
        cli = '{} list'.format(self.m_cli)
        l = subprocess.check_output(cli, shell=True, universal_newlines=True)
        mocks_list = l.split('\n')
        mocks_list = list(filter(None, mocks_list))
        ml = mocks_list[2:]
        return ml

    def get_mockservices(self):
        self.mocks = []
        ml = self.get_data_from_cli()
        for i in ml:
            ls = []
            v = i.split()
            if len(v) == 9:
                ls.append(v[0])
                ls.append(v[8])
                ls.append(v[6])
                ls.append(v[7])
                if v[2] == 'online':
                    self.mocks.append(ls)
            else:
                config.logger.error('{} - Nested Path not mentioned'.format(v[0]))
        return self.mocks

    def generate_dynamic_config(self):
        d_conf = {
            'http': {
                'routers': {},
                'services': {}
            }
        }
        mocks = self.get_mockservices()
        for mock in mocks:
            rule = 'Host(`{}`) && PathPrefix(`/{}`)'.format(
                self.t_url,
                mock[1]
            )
            router = {'rule' : rule, 'service' : mock[0],
                'entryPoints' : 'websecure', 'tls': {}}
            url = 'http://{}:{}'.format(mock[2], mock[3])
            service = {'loadBalancer': {'servers': [{'url': url }]}}
            d_conf['http']['routers'][mock[0]] = router
            d_conf['http']['services'][mock[0]] = service
        return d_conf

def generate_json():
    v = MockoonCLI()
    conf = v.generate_dynamic_config()
    return json.dumps(conf)

def generate_yaml():
    v = MockoonCLI()
    conf = v.generate_dynamic_config()
    return yaml.dump(conf)

if __name__ == '__main__':
    generate_yaml()
