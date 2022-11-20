from scht2.onos_config import OnosConfigurator

if __name__ == "__main__":
	configurator = OnosConfigurator("http://192.168.16.46:8181/onos/v1", ('onos', 'rocks'))
	configurator.load_flows()
	configurator.load_devices()
	configurator.load_links()
	configurator.clear(10)