from lxml import objectify
import os
class obj(dict):
    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]
class Configuration():

    def __init__(self):
        xmlFile = os.path.dirname(os.path.abspath(__file__)) + "/../config/config.xml"

        try:
            with open(xmlFile) as f:
                xml = f.read()
        except:
            raise Exception("[config] Cannot read config file from:{}".format(xmlFile))

        self._config = objectify.fromstring(xml)
        self.settings = self._config.settings
        self.repos = self._readRepos()

    def _readRepos(self):
        repos = {}
        for repo in self._config.repos.getchildren():
            name = str(repo.attrib["name"]).lower()
            repos[name] = obj()
            repos[name].name = name
            repos[name].path = str(repo.attrib["path"]).lower()
        return repos