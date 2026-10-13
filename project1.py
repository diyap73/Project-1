
def initialize():

    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.

    '''

    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global good_battery_health
    
    cur_time = 0
    cur_charge = 50
    cur_temp = 20
    good_battery_health = True

def simulate_activity(activity, duration):
    pass

def duration_fast_charge_possible():
    minutes_fast_charge_possible = 0
    minutes_fast_charge_possible_charge = 0
    minutes_fast_charge_possible_temp = 0
    # while battery_health and cur_temp <= 40 and cur_charge < 80:
    #     cur_charge += 3
    #     cur_temp += 0.5
    if battery_health == True:

        if cur_charge < 80:
                minutes_fast_charge_possible_charge += 1 * (80 - cur_charge) / 3
        if cur_temp < 40:
                minutes_fast_charge_possible_temp += 1 * (40 - cur_temp) / 0.5
        if minutes_fast_charge_possible_temp < minutes_fast_charge_possible_charge:
                minutes_fast_charge_possible = minutes_fast_charge_possible_temp
        else:
                minutes_fast_charge_possible = minutes_fast_charge_possible_charge


    return minutes_fast_charge_possible

def get_cur_temp():
    global cur_temp
    cur_temp = float(cur_temp)
    return cur_temp

def get_cur_charge():
    global cur_charge
    cur_charge = float(cur_charge)
    return cur_charge

def get_cur_battery_health():
    pass
    
def charge_time_needed(minutes):
    time_needed = 2 * minutes
    if cur_charge > time_needed:
        return 0
    if time_needed > 100:
        return None
        
    # bad battery health, can only slow charge
    if battery_health == False:
        if time_needed > 80:
            return None
        else:
            return(time_needed - cur_charge)
    # good battery health, fast charging until 80% and then slow charging
    else:
        # finding if the fast charge duration is smaller because of smth like the temperature or battery health
        fast = min(duration_fast_charge_possible(), ((time_needed - cur_charge) / 3))
        cur_charge_after_fast = cur_charge + 3 * fast
        # slow charge for the time remaining after the fast charge
        slow = time_needed - cur_charge_after_fast
        return(fast + slow)

if __name__ == '__main__':

    initialize()

    print(duration_fast_charge_possible()) # 10
    print(charge_time_needed(50)) # 30

    simulate_activity("charge",30)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 30

    simulate_activity("use",50)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 80

    simulate_activity("use",10)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 70

    simulate_activity("charge",100)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 95

    simulate_activity("idle",100)
    print(get_cur_charge()) # 50
    print(get_cur_temp()) # 0
    print(get_cur_battery_health()) # True
    print(duration_fast_charge_possible()) # 10

    simulate_activity("charge",80)
    print(get_cur_charge()) # 90
    print(get_cur_temp()) # 22.5
    print(get_cur_battery_health()) # False

    simulate_activity("use",40)
    print(get_cur_charge()) # 10
    print(get_cur_temp()) # 62.5

    simulate_activity("charge",80)
    print(get_cur_charge()) # 80
    print(get_cur_temp()) # 82.5

    initialize()

    # add your tests here
