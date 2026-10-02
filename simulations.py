import game_engine as bj
import strategies as strats

num_decks = 6

my_Shoe = bj.Shoe(num_decks) 

N = 100000
total = 0

#Test functions for three easy strategies

'''
for n in range (0, N):
    result = bj.play_round(my_Shoe, strats.always_stand)
    total += result



for n in range (0, N):
    result = bj.play_round(my_Shoe, strats.always_hit_u17)
    total += result



for n in range (0, N):
    result = bj.play_round(my_Shoe, strats.always_hit)
    total += result

print(total/N)


'''