# Take Home Project By Sebastian Moncada Duque

Here is the part 2 explanation.

## A. Script’s Logic

1. First I started with a manual validation of the information to understand what information I had and to see errors in the data to correct.
2. Because some of the rows had empty spaces I created a function called "clean_data" where it goes through the rows one by one and if it finds an empty mail it adds one by default "notprovided@verify.email", if it finds an empty foundation date it adds "01.01.1900" and if it finds an empty revenue it adds "0". All this to avoid problems when injecting the information through the API.
3. To get the list of all the leads I go row by row checking the name of the company and adding them to a list and every time I find a company that I don't have yet on the list I add it.
4. to obtain the states I go through the rows one by one and each state that is not yet in my list I add it, then I go through each row of the data again and I compare it with each of the states. For this process in a variable called "accumulator" I add all the revenue of all the leads of the state, in a variable called "counter" I add 1 to indicate another lead for that state, and in another variable I save the highest revenue, so at the end of the process I get all this information, I save it in a list and I can continue with the same process but with the next state.

### NOTE:
I started creating everything from scratch but when reviewing I discovered that you already had a repository with sample scripts and one of them was to get the information from a CSV file and inject them using the API grouping the contacts by leads, so I decided to use it, but you will also find the functions that I developed that do the same, only they don't do the API injection

## B. How to run the script?

1. Clone the repo `git clone https://github.com/sebas6612/take_home_project.git`
2. `cd take_home_project`
3. make sure to have the CSV file inside the folder, in my case named: "MOCK_DATA.csv"
4. `pip install -r requirements.txt`
5. `python Close_API.py`
6. `python csv_to_cio.py -k [API.KEY] MOCK_DATA_CLEANED.csv` put your API key