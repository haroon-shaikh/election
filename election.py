

import csv
import os
import time
from datetime import datetime as dt
from collections import defaultdict
import pprint

def read_csv(path):
    """
    Reads the CSV file at path, and returns a list of rows. Each row is a
    dictionary that maps a column name to a value in that column, as a string.
    """
    output = []
    for row in csv.DictReader(open(path)):
        output.append(row)
    return output




def row_to_edge(row):
    """
    Given an election result row or poll data row, returns the Democratic edge
    in that state.
    """
    return float(row["Dem"]) - float(row["Rep"])

def state_edges(election_result_rows):
    """
    Given a list of election result rows, returns state edges.
    The input list does has no duplicate states;
    that is, each state is represented at most once in the input list.
    """
    lead={}
    for x in election_result_rows:
        edge=float(row_to_edge(x))
        state=x["State"]
        lead.update({state:edge})
    return lead






def earlier_date(date1, date2):

 
    return (time.strptime(date1, "%b %d %Y") < time.strptime(date2, "%b %d %Y"))

def most_recent_poll_row(poll_rows, pollster, state):
    
    latestdate=None
    latestpoll=None
    for x in poll_rows:
        if x.get("State")==state and x.get("Pollster")==pollster:
            if latestdate==None:
                latestdate=x.get("Date")
            if latestpoll==None:
                latestpoll=x
            if earlier_date(latestdate,x.get("Date")):
                latestdate=x.get("Date")
                latestpoll=x


    return latestpoll


def unique_column_values(rows, column_name):

    #TODO: Implement this function
    a=set()
    for x in rows:
        a.add(x.get(column_name))
    return a

def pollster_predictions(poll_rows):
    
   
    prediction = {}
    pollsters = unique_column_values(poll_rows, 'Pollster')
    states = unique_column_values(poll_rows, 'State')
    for pollster in pollsters:
        prediction[pollster] = {}
        for state in states:
            recent = [most_recent_poll_row(poll_rows, pollster, state)]
            if recent != [None]:
                prediction[pollster][state] = state_edges(recent)[state]
    return prediction


def average_error(state_edges_predicted, state_edges_actual):
    """
    Given predicted state edges and actual state edges, returns
    the average error of the prediction.
    """
    predicted=[]
    actual=[]
    sum=0
    for x in state_edges_predicted:
        predicted.append(x)
        a=(state_edges_predicted[x])
        b=(state_edges_actual[x])
        difference=abs(a-state_edges_actual[x])
        sum+=difference
    average=sum/len(predicted)
    return average

  

def pollster_errors(pollster_predictions, state_edges_actual):
    
    dictionary={}
    for x in pollster_predictions:
        dictionary[x]=average_error(pollster_predictions[x],state_edges_actual)
    return dictionary
    #TODO: Implement this function





def pivot_nested_dict(nested_dict):
    """
    Pivots a nested dictionary, producing a different nested dictionary
    containing the same values.
    The input is a dictionary d1 that maps from keys k1 to dictionaries d2,
    where d2 maps from keys k2 to values v.
    The output is a dictionary d3 that maps from keys k2 to dictionaries d4,
    where d4 maps from keys k1 to values v.
    For example:
      input = { "a" : { "x": 1, "y": 2 },
                "b" : { "x": 3, "z": 4 } }
      output = {'y': {'a': 2},
                'x': {'a': 1, 'b': 3},
                'z': {'b': 4} }
    """
     #TODO: Implement this function

    d = {}
    for key, value in nested_dict.items():
        for ikey, ivalue in value.items():
            d.setdefault(ikey,{})[key] = ivalue
    return d




def average_error_to_weight(error):
    """
    Given the average error of a pollster, returns that pollster's weight.
    The error must be a positive number.
    """
    return error ** (-2)

DEFAULT_AVERAGE_ERROR = 5.0

def pollster_to_weight(pollster, pollster_errors):
    """"
    Given a pollster and a pollster errors, return the given pollster's weight.
    """
    if pollster not in pollster_errors:
        weight = average_error_to_weight(DEFAULT_AVERAGE_ERROR)
    else:
        weight = average_error_to_weight(pollster_errors[pollster])
    return weight


def weighted_average(items, weights):
    
    assert len(items) > 0
    assert len(items) == len(weights)
    sum=0
    sum2=0
    for i in range(0,len(items)):
        product=items[i]*weights[i]
        sum+=product
        sum2+=weights[i]
    return sum/sum2

    #TODO: Implement this function
    pass


def average_edge(pollster_edges, pollster_errors):




    list=[]
    for x in pollster_errors:
        list.append(pollster_errors[x])
    list2=[]
    for x in pollster_edges:
         list2.append((pollster_edges[x]))
    if len(list2) != len(list):
        
    b=weighted_average(list2,list)
    print(type(b))
    print(b)
    print(list2)
    print(list)
    return int(b)





def predict_state_edges(pollster_predictions, pollster_errors):
    """
    Given pollster predictions from a current election and pollster errors from
    a past election, returns the predicted state edges of the current election.
    """
    #TODO: Implement this function
    pass




def electoral_college_outcome(ec_rows, state_edges):
   
    ec_votes = {}              
    for row in ec_rows:
        ec_votes[row["State"]] = float(row["Electors"])

    outcome = {"Dem": 0, "Rep": 0}
    for state in state_edges:
        votes = ec_votes[state]
        if state_edges[state] > 0:
            outcome["Dem"] += votes
        elif state_edges[state] < 0:
            outcome["Rep"] += votes
        else:
            outcome["Dem"] += votes/2.0
            outcome["Rep"] += votes/2.0
    return outcome


def print_dict(dictionary):
    
    for key in sorted(dictionary.keys()):
        value = dictionary[key]
        if type(value) == float:
            value = round(value, 8)
        print (key, value)


def main():
   
    # Read state edges from the 2008 election
    edges_2008 = state_edges(read_csv("data/2008-results.csv"))

    polls_2008 = pollster_predictions(read_csv("data/2008-polls.csv"))
    polls_2012 = pollster_predictions(read_csv("data/2012-polls.csv"))

    error_2008 = pollster_errors(polls_2008, edges_2008)

    # Predict the 2012 state edges
    prediction_2012 = predict_state_edges(polls_2012, error_2008)

    # Obtain the 2012 Electoral College outcome
    ec_2012 = electoral_college_outcome(read_csv("data/2012-electoral-college.csv"),
                                        prediction_2012)

    print("Predicted 2012 election results:")
    print_dict(prediction_2012)
    print

    print ("Predicted 2012 Electoral College outcome:")
    print_dict(ec_2012)
    print



if __name__ == "__main__":
    main()
