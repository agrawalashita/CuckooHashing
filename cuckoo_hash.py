# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		
		#checking if key exists in the hash table
		for table_id in range(2):
			for existing_key in self.tables[table_id]:
				if existing_key == key:
					return True 
		
		current_table = 0
		count = 0

		while count <= self.CYCLE_THRESHOLD:

			position = self.hash_func(key, current_table)

			#if hashed position is empty
			if self.tables[current_table][position] is None:
				self.tables[current_table][position] = key
				return True
		
			#if position is occupied, we swap keys
			key, self.tables[current_table][position] = self.tables[current_table][position], key

			current_table = 1 - current_table
			count += 1
			
		print("Cycle threshold exceeded, insertion failed")
		return False

	def lookup(self, key: int) -> bool:
		if key is None:
			return False
		
		position0 = self.hash_func(key, 0)
		position1 = self.hash_func(key, 1)

		if self.tables[0][position0] == key or self.tables[1][position1] == key:
			return True		
		return False
		
	def delete(self, key: int) -> None:
		if key is None:
			return False
		
		position0 = self.hash_func(key, 0)
		position1 = self.hash_func(key, 1)

		if self.tables[0][position0] == key:
			self.tables[0][position0] = None
			return True
		elif self.tables[1][position1] == key:
			self.tables[1][position1] = None
			return True
		
		return False

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		
		old_tables = self.tables
		self.tables = [[None]*new_table_size for _ in range(2)]

		for table in old_tables:
			for key in table:
				if key is not None:
					self.insert(key)


	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define