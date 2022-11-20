from onos_config import OnosConfigurator

if __name__ == "__main__":
	configurator = OnosConfigurator("http://192.168.16.46:8181/onos/v1", ('onos', 'rocks'))
	configurator.load_flows()
	configurator.load_devices()
	configurator.load_links()

	configurator.configurate(
		['of:0000000000000002', 'of:0000000000000001', 'of:0000000000000003', 'of:0000000000000006'],
		'00:00:00:00:00:02',
		'00:00:00:00:00:06'
	)