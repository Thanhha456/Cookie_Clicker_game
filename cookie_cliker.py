"""
Cookie Clicker Simulator
"""


import math
# Used to increase the timeout, if necessary
# import codeskulptor
#
# codeskulptor.set_timeout(20)

import poc_clicker_provided as provided
import matplotlib.pyplot as plt

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._current_cookies = 0.0
        self._total_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._cost = 0.0
        self._current_state = ""
        self._history = [(self._current_time, None, self._cost, self._total_cookies)]

    def __str__(self):
        """
        Return human readable state
        """
        self._current_state = "\n" + "Current time: " + str(self._current_time) + "\n"
        self._current_state += "Current Cookies: " + str(self._current_cookies) + "\n"
        self._current_state += "CPS: " + str(round(self._current_cps, 2)) + "\n"
        self._current_state += "Total Cookies: " + str(self._total_cookies)

        return  self._current_state

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history = list(self._history)
        return history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self.get_cookies():
            return 0.0
        time_left = math.ceil((cookies - self.get_cookies())/self._current_cps)
        return time_left

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            cookies = self._current_cps * time
            self._current_cookies += cookies
            self._total_cookies += cookies


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cps += additional_cps
            self._current_cookies -= cost
            self._history.append((self._current_time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_clone = build_info.clone()
    clicker = ClickerState()
    time_left = duration - clicker.get_time()
    while time_left >= 0:
        current_cps = clicker.get_cps()
        current_cookies = clicker.get_cookies()
        current_history = clicker.get_history()

        item = strategy(current_cookies, current_cps, current_history, time_left, build_clone)

        if item == None:
            clicker.wait(time_left)
            break
        else:
            item_cost = build_clone.get_cost(item)
            item_cps = build_clone.get_cps(item)
            time_wai_till = clicker.time_until(item_cost)
            if time_wai_till == 0:
                clicker.buy_item(item, item_cost, item_cps)
                build_clone.update_item(item)
                item_cost = build_clone.get_cost(item)
                time_wai_till = clicker.time_until(item_cost)
            else:
                clicker.wait(time_wai_till)
                clicker.buy_item(item, item_cost, item_cps)
                build_clone.update_item(item)
                time_left = duration - clicker.get_time()
    history = clicker.get_history()
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items_list = build_info.build_items()
    costs_list = []
    for item in items_list:
        if cookies + cps * time_left >= build_info.get_cost(item):
            costs_list.append((build_info.get_cost(item), item))
    if costs_list:
        min_cost, min_item = min(costs_list)
        return min_item
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items_list = build_info.build_items()
    costs_list = []
    for item in items_list:
        if cookies + cps*time_left >= build_info.get_cost(item):
            costs_list.append((build_info.get_cost(item), item))
    if costs_list:
        max_cost, max_item = max(costs_list)
        return max_item
    return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """

    items_list = build_info.build_items()
    ratio_list =[]
    for item in items_list:
        if cookies + cps * time_left >= build_info.get_cost(item):
            cps_cost_proportion = build_info.get_cps(item)/build_info.get_cost(item)
            ratio_list.append((cps_cost_proportion, item))
    if ratio_list:
        ratio_list.sort(reverse=True)
        return ratio_list[0][1]
    return None



def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print(strategy_name, ":", state)

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it
    # #
    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # plt.plot(history)
    # plt.title(strategy_name)
    # plt.xlabel('Time')
    # plt.ylabel('Total Cookies')
    # plt.show()


def run():
    """
    Run the simulator.
    """
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # run_strategy("None", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)

run()



