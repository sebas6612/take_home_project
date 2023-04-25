# Take Home Project By Sebastian Moncada Duque

Here is the part 2 explanation.

## A. Script’s Logic

1. First I started with a manual validation of the information to understand what information I had and to see errors in the data to correct.
2. Because some of the rows had empty spaces I created a function called "clean_data" where it goes through the rows one by one and if it finds an empty mail it adds one by default "notprovided@verify.email", if it finds an empty foundation date it adds "01.01.1900" and if it finds an empty revenue it adds "0". All this to avoid problems when injecting the information through the API.
3. To get the list of all the leads and States, I go row by row checking the name of the company and adding them to a list and every time I find a company that I don't have yet on the list I add it, the same with the States list.
4. To obtain the list of the Leads that were founded between 2 dates, I make a "Post" API call where the parameters filters that and the API responds with that list.
5. In order to get the inform of the States revenue, first I make a "Post" API call where the parameters let me get the list of the Leads of that specific State and where the revenue is greater than "0". During this iteration process I have a variable called "accumulator" where I add all the revenue of all the leads of the state, and in another variable I save the highest revenue, so at the end of the process I get all this information, I save it in a list and I can continue with the same process but with the next state.


## B. How to run the script?

1. Clone the repo `git clone https://github.com/sebas6612/take_home_project.git`
2. `cd take_home_project`
3. make sure to have the CSV file inside the folder, in my case named: "MOCK_DATA.csv"
4. `pip install -r requirements.txt`
5. `python Close_API.py`