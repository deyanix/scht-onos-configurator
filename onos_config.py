import json
import requests


class OnosConfigurator:
	devices = []
	flows = []
	links = []

	def __init__(self, base_url, auth):
		self.base_url = base_url
		self.auth = auth

	def load_flows(self):
		self.flows = requests.get(f"{self.base_url}/flows", auth=self.auth).json()['flows']

	def load_devices(self):
		self.devices = requests.get(f"{self.base_url}/devices", auth=self.auth).json()['devices']

	def load_links(self):
		self.links = requests.get(f"{self.base_url}/links", auth=self.auth).json()['links']

	def get_device(self, id):
		filtered = [device for device in self.devices if device['id'] == id]
		if len(filtered) > 0:
			return filtered[0]
		return None

	def clear_flows(self, n=1):
		for flow in self.flows:
			flow_id = flow['id']
			device_id = flow['deviceId']
			print("Cleared flow", device_id)
			for i in range(n):
				requests.delete(f"{self.base_url}/flows/{device_id}/{flow_id}", auth=self.auth)

	def clear_devices(self, n=1):
		for device in self.devices:
			device_id = device['id']
			print("Cleared device", device_id)
			for i in range(n):
				requests.delete(f"{self.base_url}/devices/{device_id}", auth=self.auth)

	def clear(self, n=1):
		self.clear_devices(n)
		self.clear_flows(n)

	def configure_flow(self, device_id, src_mac, dst_mac, dst_port):
		flow_config = {
			"priority": 40000,
			"timeout": 0,
			"isPermanent": True,
			"deviceId": device_id,
			"treatment": {
				"instructions": [
					{"type": "OUTPUT", "port": dst_port}
				]
			},
			"selector": {
				"criteria": [
					{
						"type": "ETH_SRC",
						"mac": src_mac
					},
					{
						"type": "ETH_DST",
						"mac": dst_mac
					}
				]
			}
		}
		res = requests.post(f"{self.base_url}/flows/{device_id}", data=json.dumps(flow_config), auth=self.auth)
		return res.status_code

	def configure_host(self, mac, ip, device_id, port):
		payload = {
			"mac": mac,
			"vlan": "None",
			"ipAddresses": [ip],
			"locations": [
				{
					"elementId": device_id,
					"port": port
				}
			],
			"auxLocations": [],
			"innerVlan": "None",
		}
		res = requests.post(f"{self.base_url}/hosts", data=json.dumps(payload), auth=self.auth)
		return res.status_code

	def configurate(self, path, src_mac, dst_mac):
		self.configure_flow(path[-1], src_mac, dst_mac, 1)
		self.configure_flow(path[0], dst_mac, src_mac, 1)
		for i in range(len(path)-1):
			src_device = path[i]
			dst_device = path[i+1]
			for link in self.links:
				if link['src']['device'] == src_device and link['dst']['device'] == dst_device:
					self.configure_flow(src_device, src_mac, dst_mac, link['src']['port'])
					self.configure_flow(dst_device, dst_mac, src_mac, link['dst']['port'])
