This project for assessment in "Principles of Computing (Part 1)" course at Rice university.  
https://www.coursera.org/learn/principles-of-computing-1?specialization=computer-fundamentals  

**MiniProject: Cookie_clicker**  

*Overview*  

Cookie Clicker is a game built around a simulation in which your goal is to bake as many cookies as fast as possible. The main strategy component of the game is choosing how to allocate the cookies that you have produced to upgrade your ability to produce even more cookies faster.   
For this assignment, you will implement a simplified simulation of the Cookie Clicker game. You will implement different strategies and see how they fare over a given period of time. In our version of the game, there is no graphical interface and therefore no actual "clicking". Instead, you will start with a CPS of 1.0 and may start purchasing automatic production methods once you have enough cookies to do so. You will implement both the simulation engine for the game and your own strategies for selecting what production methods to buy.  
We have provided a BuildInfo class for you to use. This class keeps track of the cost (in cookies) and value (in CPS) of each item (production method) that you can buy. When you create a new BuildInfo object, it is initialized by default with the default parameters for our game.  
We have also provided a run function to run your simulator. Note that the run function simply calls run_strategy, which runs the simulator once with a given strategy.  

We have provided a simple strategy, called strategy_cursor_broken. Note the signature of the function: strategy_cursor_broken(cookies, cps, history, time_left, build_info). All strategy functions take the current number of cookies, the current CPS, the history of purchases in the simulation, the amount of time left in the simulation, and a BuildInfo object (even if they don't use these parameters). You'll note that this simple strategy just always picks "Cursor" no matter what the state of the game is. This is obviously not a good strategy (and it violates the requirements of a strategy function given below), but rather is a placeholder so you can see the signature of a strategy function looks like and use it while you are debugging other parts of your code.  


You should first implement the ClickerState class. This class will keep track of the state of the game during a simulation.The ClickerState class must keep track of four things:

- The total number of cookies produced throughout the entire game (this should be initialized to 0.0).
- The current number of cookies you have (this should be initialized to 0.0).
- The current time (in seconds) of the game (this should be initialized to 0.0).
- The current CPS (this should be initialized to 1.0).

Once you have a complete ClickerState class, you are ready to implement simulate_clicker. The simulate_clicker function should take a BuildInfo class, the number of seconds to run the simulation for, and a strategy function. Note that simulate_clicker is a higher-order function: it takes a strategy function as an argument!

- Check the current time and break out of the loop if the duration has been passed.
- Call the strategy function with the appropriate arguments to determine which item to purchase next. If the strategy function returns None, you should break out of the loop, as that means no more items will be purchased.
- Determine how much time must elapse until it is possible to purchase the item. If you would have to wait past the duration of the simulation to purchase the item, you should end the simulation.
- Wait until that time.
- Buy the item.
- Update the build information.  

For correctness, you should not allow the simulation to run past the duration. This means that you should not allow an item to be purchased if you would have to wait until after the duration of the simulation to have enough cookies. Further, after you have exited the loop, if there is time left, you should allow cookies to accumulate for the remainder of the time left. Note that you should allow the purchase of items at the final duration time. Also, if you have enough cookies, it is possible to purchase multiple items at the same time step. (Note that this differs from the actual Cookie Clicker game, where it is not possible to buy multiple items at the same time.) This is most likely to happen exactly at the final duration time, when a strategy might choose to buy as many items as it can, given that there is no more time left.


Finally, you should implement some strategies to select items for you game. You are required to implement the following strategies:

- strategy_cheap: this strategy should always select the cheapest item that you can afford in the time left.
- strategy_expensive: this strategy should always select the most expensive item you can afford in the time left.
- strategy_best: this is the best strategy that you can come up with.

For strategy_best, you will be graded on how many total cookies you are able to earn with the default SIM_TIME and BuildInfo. To receive full credit, you must get at least 1.30*10^18 total cookies.   

**Outcome:**

- strategy_cheap: 

Cheap :   
Current time: 10000000000.0  
Current Cookies: 149360255735977.94  
CPS: 123436706.3  
Total Cookies: 1.1528593562127876e+18  
   
- strategy_expensive: 

Expensive :   
Current time: 10000000000.0  
Current Cookies: 2414.646120757243  
CPS: 133980795.7  
Total Cookies: 6.836764434425321e+17   

- strategy_best:  

Best :   
Current time: 10000000000.0  
Current Cookies: 57028878943.21774  
CPS: 140318078.7  
Total Cookies: 1.3140188649959524e+18  
