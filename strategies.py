#Three basic strategies
def always_stand(player_hand, up_card):
        
    return 'stand'

def always_hit(player_hand, up_card):

    return 'hit'

def always_hit_u17_stand_weak_up_card(player_hand, up_card):

    total, soft = player_hand.total_value()

    if up_card <= 6:
        if total >= 12:
            return 'stand'
        else:
            return 'hit'
    else:
        if total < 17:
            return 'hit'
        else:
            return 'stand'

   