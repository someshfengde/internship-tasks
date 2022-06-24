#%%
import numpy as np
from typing import List

from wandb import _IS_INTERNAL_PROCESS

class Solution:
    def isPossible(self, target: List[int]) -> bool:
            # finding max element from target array 
            max_element = max(target)
            # sum of target list 
            sum_target = sum(target)
            # findign index of max element
            max_index = target.index(max_element)
            diff = sum_target - max_element 
            if target[max_index] == 1 or diff == 1 : return True 
            # check if all elements are equal to 1 
            if diff > target[max_index] or diff == 0 or target[max_index] % diff == 0 :return False 
            target[max_index] %= diff
            return self.isPossible(target)


s = Solution()
s.isPossible(target = [1,100000])


# %%
