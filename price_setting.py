import pandas as pd
import numpy as np
boxinfo = pd.read_excel('transport.xlsx', sheet_name = 'box')
class Transport():
	def __init__(self, weight, volume, cost = 9999):
		self.netweight = weight
		self.volume = volume
		try:
			if cost < self.min_cost:
				self.min_cost = cost
		except AttributeError:
			self.min_cost = cost

class Whole(Transport):
	def __init__(self, weight, volume):
		Transport.__init__(self, weight, volume)
		for i in range(len(boxinfo)):
			if self.volume <= boxinfo['volume'][i]:
				self.boxcost = boxinfo['cost'][i]
				self.boxweight = boxinfo['weight'][i]
				self.boxsize = boxinfo['size'][i]
				break

class Seperate(Transport):
	def __init__(self, weight, volume):
		Transport.__init__(self, weight, volume)
		self.box_count = np.ceil()

test = Whole(124123, 31312)
print(test.boxsize)
