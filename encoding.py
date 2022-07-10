###################
##  Problem 1.1	 ##
###################

def phi_1(age, feedback):
    age_encoding = {0: range(0,20),
                    1: range(20,40),
                    2: range(40,60),
                    3: range(60,80),
                    4: range(80,100)}
    
    feedback_encoding = {"happy": 5,
                         "satisfied": 6,
                         "unhappy": 7}
    
    feature_vector = [0] * 8    # initialize a feature vector of length 8
    
    # one-hot encoding for age interval
    for i, age_range in age_encoding.items():
        if age in age_range:
            feature_vector[i] = 1
            break
    
    # one-hot encoding for feedback category
    feature_vector[feedback_encoding[feedback]] = 1
    
    return feature_vector

###################
##  Problem 1.2	 ##
###################

import random

'''
The logs are formatted in the following way
          time | recorded speed | location ID
          
time            : An integer signifying a Unix timestamp.
                  You have the option to sort timestamps to derive any meaningful information
recorded_speed  : A positive integer denoting speeds in MPH
location ID     : An integer denoting a location ID

You can choose to use this list to test your solution.
'''
logs = [
        "1643733878 | 55 | 12344",
        "1643743844 | 32 | 1264",
        "1643754523 | 45 | 166",
        "1643763976 | 89 | 128569",
]

'''
Returns a random speed limit for a given location ID
You can choose to use this implementation to test your solution.
'''
def get_speed_limit(loc_id):
    speed_limits = [15, 25, 35, 45, 50, 55, 65, 75]
    r_idx = random.randint(0,len(speed_limits)-1)
    return speed_limits[r_idx]

'''
Returns a random 8 letter location name for a given location ID
You can choose to use this implementation to test your solution.
'''
def get_location_name(loc_id, length=8):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def parse_logs(logs_string):
  '''
  Helper function for phi_2 to extract the details (integers) out of the string.
  Given a single log (string), return relevant details about a user.
  
  Hint: consider using the split function to split based on a delimiter
  '''
  return logs_string.split(" | ")


def phi_2(user_log):
    '''
    Use the logs to return a list of features.
    
    Args:
      user_log (list): a list of size <num_entries> containing log strings for a given driver

    Return:
      a list of size n (n>=4), where each item in the list is a feature for the given driver

    You can assume that get_speed_limit(loc_id) and get_location_name(loc_id) provide an integer and a string respectively corresponding to a loc_id
    You can then call these functions in your code to retrieve information regarding speed limits and location names.
    '''
    # This log would contain information for one user
    parsed_logs = []
    for log in user_log:
        parsed_logs.append(parse_logs(log))
    
    
    # initialize the variables for the features
    speed_percent_diff = 0
    rush_hour_count = 0
    evening_count = 0
    risk_month_count = 0
    
    
    # iterate through every log for the use
    for log in parsed_logs:
        unix_timestamp = log[0]
        speed = log[1]
        loc_id = log[2]
        
        # compute the percent difference between the user's speed and speed_limit
        speed_limit = get_speed_limit(loc_id)
        speed_percent_diff += (int(speed) - speed_limit) / speed_limit
    
        '''
        Assume that there is a helper function convert_unix(unix_timestamp) that takes in a unix
        timestamp and returns a tuple (month, day of week, hour), where
            month ranges from 1 to 12,
            day of week is a str 'Sun', 'Mon', 'Tue', 'Thu', 'Fri', 'Sat'
            hour ranges from 1 to 24 (military time hour).
        '''
        
        month, day_of_week, hour = convert_unix(unix_timestamp)
        
        # compute if the time is during the rush hour (weekday 8-9 AM or 4-6 PM)
        if (day_of_week not in ['Sun', 'Sat']) and (hour in [8, 9, 16, 17, 18]):
            rush_hour_count += 1
            
        # compute if the time is in the evening (8 PM-12 AM)
        if hour in range(20, 25):
            evening_count += 1
        
        # compute if the month is a high-risk month (Jul, Aug, Oct)
        if month in [7, 8, 10]:
            risk_month_count += 1
    
    # initialize feature vector of length 4
    feature_vector = [0] * 4
    # populate the values of feature_vector
    feature_vector[0] = speed_percent_diff
    feature_vector[1] = rush_hour_count
    feature_vector[2] = evening_count
    feature_vector[3] = risk_month_count
    
    return feature_vector