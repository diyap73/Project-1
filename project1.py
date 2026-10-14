
def initialize():

    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global good_battery_health
    global times_overcharged

    cur_temp = 20
    cur_charge = 50
    cur_time = 0
    good_battery_health = True
    times_overcharged = []

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

    return good_battery_health

# Returns the duration for which fast charge is possible based on the current
# battery health, temperature, and charge
def duration_fast_charge_possible():

    global cur_temp, cur_charge, good_battery_health

    minutes_fast_charge_possible = 0
    # affect of max charge on max fast charge
    minutes_fast_charge_possible_charge = 0
    # affect of max temp on max fast charge
    minutes_fast_charge_possible_temp = 0

    # Checking if the battery health is good
    if good_battery_health:

        # Fast charge is possible if the current charge is less than 80
        if cur_charge < 80:
            minutes_fast_charge_possible_charge += (80 - cur_charge) / 3

        # Fast charge is possible if the temperature is less than 40
        if cur_temp >= 0 and cur_temp <= 40:
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

    # Activity: charge
    if activity == 'charge':

        for minute in range(duration):

            cur_time += 1

            # Fast charging occurs
            if cur_temp >= 0 and cur_temp <= 40 and cur_charge < 80 and \
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

                # Increase charge by 1 percent
                if cur_charge < max_charge:
                    cur_charge += 1

                    # For fractional values such as 79.5 + 1 = 80.5
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
    # total charge (in %) the battery must have for `minutes` of use,
    # since use drains 2% per minute
    charge_needed = 2 * minutes

    # already enough charge, no charging needed
    if cur_charge >= charge_needed:
        return 0

    if charge_needed > 100:
        return None

    # making local variables to not edit the global variables
    charge = cur_charge
    temp = cur_temp
    time = cur_time
    health = good_battery_health
    overcharges = list(times_overcharged)

    overcharged = False
    # number of minutes of charging simulated so far
    minutes_charged = 0

    while charge < charge_needed:
        time += 1
        minutes_charged += 1
        # save the charge before this minute, to check later if it increased
        charge_before = charge
        
        # fast charge
        if temp >= 0 and temp <= 40 and charge < 80 and health:
            charge += 3
            temp += 0.5

            if charge > 100:
                charge = 100

        else:
            if health:
                max_charge = 100
            else:
                max_charge = 80
            # slow charge
            if charge < max_charge:
                charge += 1

                # Fractional values
                # don't go past the maximum (matters for fractional charges)
                if charge > max_charge:
                    charge = max_charge

            temp += 0.25
        # Considering battery overcharging
        if health and not overcharged and charge >= 90:

            overcharged = True
            overcharges.append(time)

            if len(overcharges) >= 3 and \
                overcharges[-1] - overcharges[-3] < 360:
                health = False

        if charge == charge_before:
            return None

    return minutes_charged

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
