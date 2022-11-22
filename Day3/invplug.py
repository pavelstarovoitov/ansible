from ansible.plugins.inventory import BaseInventoryPlugin

class InventoryModule(BaseInventoryPlugin):

    NAME = 'myplugin'

def parse(self, inventory, loader, path, cache=True):

     # call base method to ensure properties are available for use with other helper methods
     super(InventoryModule, self).parse(inventory, loader, path, cache)

     # this method will parse 'common format' inventory sources and
     # update any options declared in DOCUMENTATION as needed
     config = self._read_config_data(path)

     # if NOT using _read_config_data you should call set_options directly,
     # to process any defined configuration for this plugin,
     # if you don't define any options you can skip
     #self.set_options()

     # example consuming options from inventory source
     mysession = apilib.session(user=self.get_option('api_user'),
                                password=self.get_option('api_pass'),
                                server=self.get_option('api_server')
     )


     # make requests to get data to feed into inventory
     mydata = mysession.getitall()

     #parse data and create inventory objects:
     for colo in mydata:
         for server in mydata[colo]['servers']:
             self.inventory.add_host(server['name'])
             self.inventory.set_variable(server['name'], 'ansible_host', server['external_ip'])