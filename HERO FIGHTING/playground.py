
width = 1280
height = 720
a = 170
b = 0.1

def solve(print_res=False, sub=False, left=False, add=False):
    if print_res:
        # print('a / b = a/b')
        # print('where a = {a}, b = {b}')
        print('a = desired pos, b = size (width or height)')
        print(f'{a} / {b} = {a/b}')
        # print(((a/b)*b))
        
    if left:
        x = a*b
        return x
    elif sub:
        x = a-(a*b)
        return x
    elif add:
        x = a+(a*b)
        return x
    

    
# x = []
# h = type(x)
# if h is list:
#     print('asd')
# else:
    # print('is not')
# items = [object()]

# items += [object()]

# o = []
# for i in o:
#     print('sad')
# clean = False 
# e = [['slicer', True, 100], ['archer', False, 100]]
# t = []
# for i in range(40): # acts as game loop
#     print(i)
#     for j in e: # iterate through enemy, bool means collided
#         print(f'Identifying {j}...')
#         if i == 1:
#             print(f'{e[0]} is not colliding') if not clean else None
#             e[0][1] = False
#         if i == 2:
#             print(f'{e[1]} is colliding') if not clean else None
#             e[1][1] = True
        
#         if i == 3:
#             print(f'{e[0]} is colliding') if not clean else None
#             e[0][1] = True
#         # if i == 3:
#         #     print(f'{e[1]} is not colliding') if not clean else None
#         #     e[1][1] = False
#         print('current:',t) if not clean else None
#         if j[1] and j not in t: # add enemy if enemy collided and not in targets
#             print('added', j) if not clean else None
#             t.append(j)
#             # print(t)
#         else: 
#             if j in t: # don't add enemy if enemy still collided and enemy already in targets
#                 print(f'{j} already in current') if not clean else None
#             else: # subject for remove if enemy is not collided anymore and still inside targets
#                 print('not collided') if not clean else None
#         if not j[1] and j in t: # remove enemy if enemy not collided and enemy is present in targets
#             print('removed', j) if not clean else None
#             t.remove(j)
#             # print(t)
#         else:
#             if j not in t: # don't remove when enemy is not in current, cannot remove anything
#                 print(f'{j} is not in current') if not clean else None
#             else: # don't remove if enemy still colliding
#                 print('already collided') if not clean else None
#         print('current:',t)    if not clean else None
#         print()    if not clean else None
#     print('final current:',t) if not clean else None
#     print(f'DEALING DAMAGE TO THESE: {t}')
#     for d in t: # iterate through targets
#         if len(t)>0: # make sure targets isn't empty
#             for hp in d: # iterate through enemy like dealing damage (object)
#             # print(t)
#                 d[2] -= 1
                
                
                
#                 break
            
#             continue
#         else:
#             pass
#     print('removing enemies in', t)
#     t.clear() # remove all enemies in target 
#     print(f'STATUS OF THESE: {t}')
    
        
        
import random
c = float(f'{random.random():.2f}') #chance
d = 1.3 #dmg
v = 0.5 #value
# print(f'{f'{d*(1+v):.2f}' if c < 0.2 else f'{d}'}')


hahh = True

# if hahh:
#     print('once', hahh)
#     print('twice', hahh)
#     hahh = False
#     print('thrice', hahh)
#     for i in range(5):
#         print(f'still running even {hahh} is False.')



list1 = ['a', 'b', 'c', 'd']
list2 = ['e', 'f', 'g', 'h']

# print([x for x in list1] + [x for x in list2])


# print(5 - -2)

print(f'{23.1122038601983:.2f}')

qwe = 123

# if qwe < 2:
#     print('asd')
# else:
#     raise ValueError('huh?')
from pprint import pprint
# some_value = [0, 'skill_1', ]
skills = ['skill_1', 'skill_2', 'skill_3', 'skill_4']

x = {}
for i, v in enumerate(skills):
    x[i] = v

pprint(x)
print(random.seed(12))


# print('asd')
# print(items*2)
# print(solve(add=True))
# print(solve(left=True))
# print(width-int(width*0.039)-1)

# # Animation Counts
# WATER_PRINCESS_BASIC_COUNT = 10
# WATER_PRINCESS_JUMP_COUNT = 6
# WATER_PRINCESS_RUN_COUNT = 8 
# WATER_PRINCESS_IDLE_COUNT = 7
# WATER_PRINCESS_ATK1_COUNT = 8
# WATER_PRINCESS_SP_COUNT = 14
# WATER_PRINCESS_DEATH_COUNT = 6

# WATER_PRINCESS_ATK1 = 12 - 2 # reduce frame
# WATER_PRINCESS_ATK2 = 53
# WATER_PRINCESS_ATK3 = 34
# WATER_PRINCESS_SP = 28
# # ---------------------
# # print((WATER_PRINCESS_ATK2 * 0.01) * 4 * 5)
# WATER_PRINCESS_ATK1_MANA_COST = 50
# WATER_PRINCESS_ATK2_MANA_COST = 80
# WATER_PRINCESS_ATK3_MANA_COST = 100
# WATER_PRINCESS_SP_MANA_COST = 200

# WATER_PRINCESS_ATK1_SIZE = 3
# WATER_PRINCESS_ATK2_SIZE = 0.3
# WATER_PRINCESS_ATK3_SIZE = 0.3
# WATER_PRINCESS_SP_SIZE = 1.3

