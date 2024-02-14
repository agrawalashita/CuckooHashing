# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24_A:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.table = [None]*self.table_size

	def get_rand_bucket_index(self, bucket_idx: int) -> int:
		# you must use this function when you need to evict a random key from a bucket. this function
		# randomly chooses an index from a given cell index. this ensures that the random
		# index chosen by your code and our test script match.
		#
		# for example, if you need to remove a random element from the bucket at table index 5,
		# you will call get_rand_bucket_index(5) to determine which key from that bucket to evict, i.e. if get_random_bucket_index(5) returns 2, you
		# will evict the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, func_id: int) -> int:
		# access h0 via func_id=0, access h1 via func_id=1
		key = int(str(key) + str(self.__num_rehashes) + str(func_id))
		rand.seed(key)
		result = rand.randint(0, self.table_size-1)
		return result

	def get_table_contents(self) -> List[Optional[List[int]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.table

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		for attempt in range(self.CYCLE_THRESHOLD):
			for func_id in [0, 1]:
				bucket_idx = self.hash_func(key, func_id)
				bucket = self.table[bucket_idx]

				if bucket is None:
					self.table[bucket_idx] = [key]
					return True
				
				if len(bucket) < self.bucket_size:
					bucket.append(key)
					return True
		
			bucket_idx = self.hash_func(key, 0)  # Prioritize h0 for displacement
			rand_idx = self.get_rand_bucket_index(bucket_idx)
			bucket = self.table[bucket_idx]

			if bucket and len(bucket) >= self.bucket_size:
                # Swap key with a randomly selected key in the bucket
				displaced_key = bucket[rand_idx]
				bucket[rand_idx] = key
				key = displaced_key
                # Continue with next iteration to try inserting the displaced key
				
		return False  # If cycle threshold is exceeded

	def lookup(self, key: int) -> bool:
		for func_id in [0, 1]:
			bucket_idx = self.hash_func(key, func_id)
			bucket = self.table[bucket_idx]
			if bucket is not None and key in bucket:
				return True
		return False
		

	def delete(self, key: int) -> None:
		for func_id in [0, 1]:
			bucket_idx = self.hash_func(key, func_id)
			bucket = self.table[bucket_idx]
			if bucket is not None and key in bucket:
				bucket.remove(key)
				if len(bucket) == 0:
					self.table[bucket_idx] = None
					return True
		return False

	def rehash(self, new_table_size: int) -> None:
		print("----here in rehash")
		old_table = self.table
		self.__num_rehashes += 1
		self.table_size = new_table_size
		self.table = [None] * new_table_size
		for bucket in old_table:
			if bucket is not None:
				for key in bucket:
					self.insert(key)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


