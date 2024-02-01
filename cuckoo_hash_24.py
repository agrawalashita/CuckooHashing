# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.


	# def insert(self, key: int) -> bool:
	# 	print(f"Attempting to insert key {key}")

	# 	# Check if key already exists in either of the two tables
	# 	for table_id in range(2):
	# 		bucket_idx = self.hash_func(key, table_id)
	# 		bucket = self.tables[table_id][bucket_idx]
	# 		if bucket is not None and key in bucket:
	# 			print(f"Key {key} already exists in table {table_id}, bucket {bucket_idx}")
	# 			return True 

	# 	original_key = key
	# 	current_table = 0
	# 	count = 0

	# 	while count <= self.CYCLE_THRESHOLD:
	# 		print(f"Current table: {current_table}, attempt count: {count}")

	# 		bucket_idx = self.hash_func(key, current_table)
	# 		bucket = self.tables[current_table][bucket_idx]

	# 		print(f"Key {key} hashed to bucket {bucket_idx} in table {current_table}")

	# 		if bucket is None:
	# 			self.tables[current_table][bucket_idx] = bucket = []
	# 			print(f"Initialized new bucket at index {bucket_idx} in table {current_table}")

	# 		if len(bucket) < self.bucket_size:
	# 			bucket.append(key)
	# 			print(f"Inserted key {key} into bucket {bucket_idx} in table {current_table}")
	# 			return True

	# 		rand_idx = self.get_rand_idx_from_bucket(bucket_idx, current_table)
	# 		displaced_key = bucket[rand_idx]
	# 		print(f"Bucket full, displacing key {displaced_key} from index {rand_idx} in bucket {bucket_idx}")
	# 		key, bucket[rand_idx] = displaced_key, key

	# 		current_table = 1 - current_table
	# 		count += 1

	# 		if key == original_key and count > 1:
	# 			print(f"Cycle detected while inserting key {key}, insertion failed")
	# 			return False

	# 	print(f"Cycle threshold exceeded while inserting key {key}, insertion failed")
	# 	return False

	def insert(self, key: int) -> bool:

		for table_id in range(2):
			bucket_idx = self.hash_func(key, table_id)
			bucket = self.tables[table_id][bucket_idx]
			if bucket is not None and key in bucket:
				return True 
			
		current_table = 0
		count = 0

		while count <= self.CYCLE_THRESHOLD:

			bucket_idx = self.hash_func(key, current_table)
			bucket = self.tables[current_table][bucket_idx]

			if bucket is None:
				self.tables[current_table][bucket_idx] = bucket = []

			if len(bucket) < self.bucket_size:
				bucket.append(key)
				return True
			
			rand_idx = self.get_rand_idx_from_bucket(bucket_idx, current_table)
			key, bucket[rand_idx] = bucket[rand_idx], key

			current_table = 1 - current_table
			count += 1

			#if we are back to the original key and position, it means a cycle is there, return false
			# if key == original_key and self.hash_func(key, current_table) == self.hash_func(original_key, current_table):
			# 	print("Cycle detected, insertion failed")
			# 	return False
			
		print("Cycle threshold exceeded, insertion failed")
		return False

	def lookup(self, key: int) -> bool:
		if key is None:
			return False
		
		bucket_idx0 = self.hash_func(key, 0)
		bucket0 = self.tables[0][bucket_idx0]
		if bucket0 is not None and key in bucket0:
			return True

		bucket_idx1 = self.hash_func(key, 1)
		bucket1 = self.tables[1][bucket_idx1]
		if bucket1 is not None and key in bucket1:
			return True

		return False


	def delete(self, key: int) -> None:
		if key is None:
			return False
		
		bucket_idx0 = self.hash_func(key, 0)
		bucket0 = self.tables[0][bucket_idx0]
		if bucket0 is not None and key in bucket0:
			bucket0.remove(key)
			if len(bucket0) == 0:
				self.tables[0][bucket_idx0] = None
			return True
		
		bucket_idx1 = self.hash_func(key, 1)
		bucket1 = self.tables[1][bucket_idx1]
		if bucket1 is not None and key in bucket1:
			bucket1.remove(key)
			if len(bucket1) == 0:
				self.tables[1][bucket_idx1] = None
			return True

		return False


	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		
		old_tables = self.tables

		self.tables = [[None for _ in range(new_table_size)] for _ in range(2)]

		for table in old_tables:
			for bucket in table:
				if bucket is not None:
					for key in bucket:
						if key is not None:
							self.insert(key)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


