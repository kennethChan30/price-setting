import pandas as pd
import numpy as np
boxinfo = pd.read_excel('transport.xlsx', sheet_name = 'box')
ems_large = pd.read_excel('transport.xlsx', sheet_name = 'large EMS', names = ['weight', 'fee'])
air_large = pd.read_excel('transport.xlsx', sheet_name = 'large air', names = ['weight', 'fee'])
ems_small = pd.read_excel('transport.xlsx', sheet_name = 'small EMS', names = ['weight', 'fee'])
air_small = pd.read_excel('transport.xlsx', sheet_name = 'small air', names = ['weight', 'fee'])
yamato_fee = pd.read_excel('transport.xlsx', sheet_name = 'yamato', names = ['weight', 'size', 'fee'])
products_list = pd.read_excel('products.xlsx', sheet_name = 'Sheet1')
class Transport():

	def __init__(self, weight, volume):
		self.netweight = weight
		self.volume = volume

	def totalcosts(self):
		self.totalcost = self.shipment + self.boxcost
		self.mincost()

	def mincost(self):
		global min_cost, method
		try:
			if self.totalcost < min_cost:
				min_cost = self.totalcost
				method = self.method
		except NameError:
			min_cost = self.totalcost
			method = self.method

class Whole(Transport):
	def __init__(self, weight, volume):
		Transport.__init__(self, weight, volume)
		for i in range(len(boxinfo)):
			if self.volume <= boxinfo['volume'][i]:
				self.boxcost = boxinfo['cost'][i]
				self.boxweight = boxinfo['weight'][i]
				self.boxsize = boxinfo['size'][i]
				self.totalweight = self.boxweight + self.netweight
				break
	def ems(self):
		for i in range(len(ems_large)):
			if self.totalweight <= ems_large['weight'][i]:
				self.shipment = ems_large['fee'][i]
				self.method = 'Large EMS'
				self.totalcosts()
				break
	def air(self):
		for i in range(len(ems_large)):
			if self.totalweight <= air_large['weight'][i]:
				self.shipment = air_large['fee'][i]
				self.method = 'Large air'
				self.totalcosts()
				break

	def yamato(self):
		for i in range(len(ems_large)):
			if self.totalweight <= yamato_fee['weight'][i] and self.boxsize <= yamato_fee['size'][i]:
				self.shipment = yamato_fee['fee'][i]
				self.method = 'Yamato'
				self.totalcosts()
				break

class Seperate(Transport):
	def __init__(self, weight, volume):
		Transport.__init__(self, weight, volume)
		self.boxsize = 80
		self.box_count = np.ceil(self.volume/boxinfo[boxinfo['size'] == 80]['volume'][1])
		self.boxcost = boxinfo[boxinfo['size'] == 80]['cost'][1]
		self.boxweight = boxinfo[boxinfo['size'] == 80]['weight'][1]
		while self.boxweight + self.netweight/self.box_count > 2:
			self.box_count = self.box_count + 1
		self.boxcost = self.box_count * self.boxcost
		self.remain_weight = self.netweight + self.box_count * self.boxweight
		self.full_box = 0
		while self.remain_weight > 2:
			self.remain_weight =self.remain_weight - 2
			self.full_box = self.full_box + 1
		self.remain_box = self.box_count - self.full_box
		self.averemain_weight = self.remain_weight/self.remain_box

	def ems(self):
		for i in range(len(ems_small)):
			if self.averemain_weight <= ems_small['weight'][i]:
				self.shipment = ems_small['fee'][i] * self.remain_box + ems_small['fee'][len(ems_small)-1] * self.full_box
				self.method = 'small EMS'
				self.totalcosts()
				break
	def air(self):
		for i in range(len(ems_large)):
			if self.averemain_weight <= air_small['weight'][i]:
				self.shipment = air_small['fee'][i] * self.remain_box + air_small['fee'][len(air_small)-1] * self.full_box
				self.method = 'small air'
				self.totalcosts()
				break

def price_set(i ,n , markup):
	global min_cost
	min_cost = 999999
	total_weight = products_list['weight'][i] * n
	total_volume = products_list['volume'][i] * n
	trasport_cost = Whole(total_weight, total_volume)
	trasport_cost.ems()
	trasport_cost.air()
	trasport_cost.yamato()
	trasport_cost = Seperate(total_weight, total_volume)
	trasport_cost.ems()
	trasport_cost.air()	
	selling_price = round((products_list['cost'][i] + min_cost/n) * (1 + markup) * 0.07, 2)
	price_list.append(selling_price)

price_list = []
for i in range(len(products_list)):
	price_set(i, 20, 0.1)
print(price_list)
