
def initialize():

    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global good_battery_health

    cur_temp = 20
    cur_charge = 50
    cur_time = 0
    good_battery_health = True

# Returns the current temperature of the battery, as a float
def get_cur_temp():

    global cur_temp
    cur_temp = float(cur_temp)

    return cur_temp

# Returns the current charge level of the battery, as a float
def get_cur_charge():

    global cur_charge
    cur_charge = float(cur_charge)

    return cur_charge

# Returns the health of the battery, as a boolean
def get_cur_battery_health():

    global good_battery_health

    return good_battery_health

# Returns the duration for which fast charge is possible based on the current
# battery health, temperature, and charge
def duration_fast_charge_possible():

    global cur_temp, cur_charge, good_battery_health

    minutes_fast_charge_possible = 0
    minutes_fast_charge_possible_charge = 0
    minutes_fast_charge_possible_temp = 0

    # Checking if the battery health is good
    if good_battery_health:

        # Fast charge is possible if the current charge is less than 80
        if cur_charge < 80:
            minutes_fast_charge_possible_charge += (80 - cur_charge) / 3

        # Fast charge is possible if the temperature is less than 40
        if cur_temp < 40:
            minutes_fast_charge_possible_temp += (40 - cur_temp) / 0.5

        # Checking which condition gives the smaller value
        if minutes_fast_charge_possible_temp < minutes_fast_charge_possible_charge:
            minutes_fast_charge_possible = minutes_fast_charge_possible_temp

        else:
            minutes_fast_charge_possible = minutes_fast_charge_possible_charge

    # Fast charge is impossible when battery health is bad
    else:
        minutes_fast_charge_possible = 0

    return minutes_fast_charge_possible


def simulate_activity(activity, duration):

    global cur_temp, cur_charge, cur_time, good_battery_health

    overcharged = False
    times_overcharged = []

    # Activity: charge
    if activity == 'charge':

        for minute in range(duration):

            cur_time += 1

            # Fast charging occurs
            if cur_temp > 0 and cur_temp < 40 and cur_charge < 80 and \
            good_battery_health:

                cur_temp += 0.5
                cur_charge += 3

            # Slow charging occurs
            else:

                # Assign max charge based on good / bad battery health
                if good_battery_health:
                    max_charge = 100

                # Battery can only charge to 80 % in bad battery health
                else:
                    max_charge = 80

                #
                if cur_charge < max_charge:
                    cur_charge += 1

                    # Might surpass 80
                    if cur_charge > max_charge:
                        cur_charge = max_charge

                # Temperature will rise, even when max charge is reached
                cur_temp += 0.25

            # When the battery is overcharged
            if good_battery_health and not overcharged and cur_charge >= 90:

                overcharged = True
                times_overcharged.append(cur_time)

                if len(times_overcharged) >= 3 and times_overcharged[-1] - times_overcharged[-3] < 360:
                    good_battery_health = False

    # Activity: use
    elif activity == 'use':

        for minute in range(duration):
            cur_time += 1

            # Change in temperature when battery is dead
            if cur_charge == 0:
                cur_temp -= 1

                # Battery temperature cannot go under 0
                if cur_temp < 0:
                    cur_temp = 0

            # Change in charge and temperature when battery is alive
            else:
                cur_charge -= 2

                # Battery charge cannot go under 0
                if cur_charge < 0:
                    cur_charge = 0

                cur_temp += 1

    # Activity: idle
    elif activity == 'idle':

        cur_time += duration
        cur_charge -= 0.5 * duration
        cur_temp -= 1 * duration

        # Battery charge cannot go under 0
        if cur_charge < 0:
            cur_charge = 0

        # Battery temperature cannot go under 0
        if cur_temp < 0:
            cur_temp = 0

def charge_time_needed(minutes):

    global cur_charge, battery_health

    charge_needed = 2 * minutes

    if cur_charge > charge_needed:
        return 0

    if charge_needed > 100:
        return None

    # bad battery health, can only slow charge
    if battery_health == False:

        if charge_needed > 80:
            return None

        else:
            return(charge_needed - cur_charge)
    # good battery health, fast charging until 80% and then slow charging
    else:

        # finding if the fast charge duration is smaller because of smth like the temperature or battery health
        # target reached before the fast charge limit
        if duration_fast_charge_possible() < ((charge_needed - cur_charge) / 3):
            cur_charge_after_fast = cur_charge + 3 * duration_fast_charge_possible()

        # target reached during fast charging
        else:
            cur_charge_after_fast = cur_charge + 3 * duration_fast_charge_possible()
        # slow charge for the time remaining after the fast charge
        duration_slow_charge_possible = charge_needed - cur_charge_after_fast

        return cur_charge_after_fast + duration_slow_charge_possible

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

    # add your tests here
