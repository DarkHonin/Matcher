from math import ceil, floor
import copy

class WeightedRow:
	def __init__(self, data:dict, weights:dict):
		self.data = data
		self.weights = weights

	@property
	def weight(self):
		ret = 0
		for cell, mod in self.weights.items():
			if(isinstance(self.data[cell], str)):
				ret +=  sum(map(ord, self.data[cell])) * mod
			if (isinstance(self.data[cell], list)):
				ret += sum(self.data[cell])
			else:
				ret += self.data[cell] * mod
		return ret

class SearchPage:
	def __init__(self, lst:list, pool:dict):
		self.rows = lst
		self.pool = pool


	@property
	def median(self):
		ret = {}
		ltlen = len(self.rows)
		i = (ltlen - 1) / 2
		for cell in self.pool:
			if isinstance(i, float):
				r1 = self.rows[floor(i)].data[cell]
				r2 = self.rows[ceil(i)].data[cell]
				if isinstance(r1, str):
					ret[cell] = (sum(map(ord, r1)) + sum(map(ord, r2))) / 2
				else:
					ret[cell] = (r1 + r2) / 2
			else:
				ret[cell] = self.rows[int(i)].data[cell]
		return ret

	def samplePoolMedian(self):
		med = self.median
		ret = []
		for e in self.rows:
			for k, dev in self.pool.items():
				if isinstance(e.data[k], str):
					val = sum(map(ord, e.data[k]))
				else:
					val = e.data[k]
				if (med[k] - dev) < val < (med[k] + dev):
					ret.insert(0, e)
		return ret

	def samplePoolDelta(self):
		ret = []
		for d in self.rows:
			for e in self.rows:
				delta = {}
				if e is not d:
					for k, dev in self.pool.items():
						if isinstance(e.data[k], str):
							val1 = sum(map(ord, e.data[k]))
							val2 = sum(map(ord, d.data[k]))
						else:
							val1 = e.data[k]
							val2 = d.data[k]
						if isinstance(val1, list):
							delta = abs(sum(set(val1) - set(val2)))
						else:
							delta = abs(val1 - val2)
						if e not in ret:
							if delta <= dev or dev is False:
								ret.insert(0, e)
		return ret


class SearchEngine:
	def __init__(self, data:list, scope:int, pool:dict, weights:dict):
		self.data = data
		self.scope = scope
		if scope > len(data):
			self.scope = len(data)
		self.pool = pool
		self.weights = weights
		self.pages = ceil(len(data) / scope)

	def search(self):
		ret = []
		for i in range(0, self.pages):
			page = self.data[i * self.scope : (i + 1) * self.scope]
			srt = self.wheightSort(page)
			if self.pool:
				sample = srt.samplePoolDelta()
			else:
				sample = srt.rows
			ret += [q.data for q in sample]
		return ret

	def wheightSort(self, data:list):
		holder = []
		for i in data:
			holder.append(WeightedRow(i, self.weights))
		holder.sort(key=lambda x : x.weight)
		return SearchPage(holder, self.pool)