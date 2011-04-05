class KeyValue:
	def __init__(self,key,value):
		self.key=key
		self.value = value

# hash table consists of a list of keyValue pairs
class HashTable:
	def __init__(self):
		self.key_value_list=[]
	def set(self,key,value):
		keyValue= KeyValue(key,value)
		self.key_value_list.append(keyValue)
	def get(self,key):
		# get the value referred to by key
		i=0
		while i<len(self.key_value_list):
			if self.key_value_list[i].key==key:
				return self.key_value_list[i].value
			i=i+1
		return None
	def get_keys(self):
		list = []
		for i in self.key_value_list: #range(0, len(self.key_value_list):
			#list.append(self.key_value_list[i].key)
			list.append(i.key)
		return list


# main
##keyValue = KeyValue("Jones","123")
#hash = HashTable()
#hash.set("Jones","123")
#hash.set("Smith","456")
#print hash.get("Smith")
