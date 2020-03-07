# ---------------------------------------------------------------------------- #
# Title: Assignment 07
# Description: Demonstrating Pickling and Error Handling in python
# ChangeLog (Who,When,What):
# KBurdette,2.3.2020, Started Code for Assignment
# ---------------------------------------------------------------------------- #

# Import

import pickle


# Data ---------------
strMovieFileName = "MovieReview.dat"
strTVShowFileName = "TVReview.dat"
filetoUse = ""
WorkingDataDict = {}

# Processing Fucntions #################################
def load_reviews_from_file(file_name):
    """ Reads pickled data from a file into a list of dictionary rows

    :param file_name: (string) with name of file:
    :return: Did it work string, Review Dictionary
    """
    # Open File
    try:
        # Open File in read byte mode
        objFile = open(file_name,"rb")
        # Use pickle module to load data into dictionary
        LocalDict = pickle.load(objFile)
        objFile.close()
        return file_name + " file loaded", LocalDict
    except FileNotFoundError:
        # If file does not exist, create new file and empty dictionary, tell user that was done
        LocalDict = {}
        otherobjFile = open(file_name, "wb")
        otherobjFile.close()
        return "No Such File, Created New Dictionary", LocalDict
    except EOFError:
        # Empty data file, build new empty dictionary
        LocalDict = {}
        return "I have an empty file. Please add a review", LocalDict
    except Exception as e:
        return str(e), {}


def show_all_items_reviewed(ReviewDict):
    """ Return List of items reviewed

    :param ReviewDict:
    :return: Return value saying list is complete
    """
    display_value("Here are all the things you've reviewed:")
    AllKeys = ReviewDict.keys()
    for things in AllKeys:
        display_value(things)
    return "That is the complete list"


def save_reviews_to_file(file_name,ReviewDict):
    """ Writes pickled data to a file

    :param file_name: (string) with name of file:
    :param ReviewDict: Dictionary to write to file
    :return: Did it work string
    """
    # Open File
    otherobjFile = open(file_name, "wb")
    pickle.dump(ReviewDict,otherobjFile)
    otherobjFile.close()
    # Pickle
    # Write Data
    return "Successfully saved file"
    # Close File


def add_review(title,textreview,ReviewDict):
    """ Add Review To List

    :param title: (string) with name of reviewed item:
    :param textreview: (string) how I felt about the title
    :param ReviewDict: Dictionary to add review to
    :return: Did it work string, Review Dictionary
    """
    # Convert Title/Review to dictionary object, will replace review if title already in dictionary
    ReviewDict[title] = textreview
    return "Added review for: " + title, ReviewDict
    # Append to list_of_reviews


def retrieve_review(key,ReviewDict):
    """ Add Review To List

    :param title: (string) with name of reviewed item:
    :param ReviewDict: Dictionary of Reviews
    :return: Did it work string, text of review
    """
    try:
        # Find key in dictionary
        reviewtext = ReviewDict[key]
        return "Here is your review for: " + key + "\n" + reviewtext + "\n"
    except KeyError:
        # If not found, exception gets triggered
        return "No review exists for: " + key
    except Exception as e:
        print(str(e))
        return "Another error occurred while finding your review"


# Presentation Functions #######################################
def display_value(printme):
    """ Print function

    :param printme:
    :return: nothing
    """
    print(printme)


def get_title_review_pair():
    """ Ask User What To Do

    No Parmeters
    :return: two text elements, title and review
    """
    TitleName = input("What is the title of what you wish to review: ")
    TextofReview = input("What did you think: ")
    return TitleName, TextofReview


def display_menu():
    """ Show users available options

    No Parameters
    No Returns
    """
    # Print Menu
    print("\t\tUser Menu For Reviews")
    print("\t\tType '1' to show a list of all reviewed items")
    print("\t\tType '2' to add a review")
    print("\t\tType '3' to show a review for an item")
    print("\t\tType '4' to switch review files")
    print("\t\tType '5' to save your current reviews to file")
    print("\t\tType '6' to exit the program")


def confirm_user_choice():
    """ Ask User to confirm choice

    :return: Text of users choice
    """
    choice = input("This will erase any unsaved changes.  Type 'y' to confirm: ")
    return choice


def ask_user_for_task():
    """ Ask User What To Do

    :return: Text of users choice
    """
    # Ask user for menu input, test it make sure it is valid
    choice = 0
    while choice not in ["1","2","3","4","5","6"]:
        choice = input("Which menu selection do you want (1-6): ")
    return choice


def which_review():
    """

    :return: User inputted task
    """
    whichtask = input("Which review to you want to see: ")
    return whichtask


def ask_user_for_topic():
    """ Starts Program, Ask User Which Reviews to work with
        Also executes if user decides to switch review files

    :return: Text of users choice
    """
    # Display Purpose
    # Ask for Choices
    print("This program allows the user to track reviews of items.")
    print("It will load your reviews from a file into a dictionary.")
    print("It currently works for TV shows and movies.")

    # dummy value to test in while loop while gathering input
    pickedmedia = ""

    # Ensures that user picks a supported review type
    # Could easily be adjusted to add user generated files
    while (pickedmedia != "1" and pickedmedia != "2"):
        pickedmedia = input("Type '1' for TV shows or '2' for movies: ")

    return pickedmedia

# Main ######################################################
# Default User value set to run data load the first time through while loop
UsersChoice = "4"

# User task function returns value 1-6
while True:
    # Sets default return code as blank
    Returncode =""

    # Shows all items in current Review Dictionary
    if UsersChoice == "1":
        Returncode = show_all_items_reviewed(WorkingDataDict)

    # Adds new review to current Dictionary
    elif UsersChoice == "2":
        title, review = get_title_review_pair()
        Returncode, WorkingDataDict = add_review(title,review,WorkingDataDict)

    # Gets new review from user, adds to dictionary
    elif UsersChoice == "3":
        mytask = which_review()
        Returncode = retrieve_review(mytask,WorkingDataDict)

    # Loads Dictionary from file
    elif UsersChoice == "4":
        # filetoUse is global variable initially set blank
        # the first time through the program, we don't need to confirm with user
        # if they want to load data
        # subsequent calls of this option, when a file is guaranteed to be set
        # it confirms with the user that any unsaved changes will be lost
        if filetoUse != "":
            useryn = confirm_user_choice()
            if useryn.lower() != "y":
                UsersChoice = ask_user_for_task()
                continue

        # Asks User for topic then sets the appropriate file name
        whichtype = ask_user_for_topic()
        if whichtype == "1":
            filetoUse = strTVShowFileName
        elif whichtype == "2":
            filetoUse = strMovieFileName

        Returncode, WorkingDataDict = load_reviews_from_file(filetoUse)

    # Saves Dictionary to File
    elif UsersChoice == "5":
        Returncode = save_reviews_to_file(filetoUse,WorkingDataDict)

    # Exits program
    elif UsersChoice == "6":
        useryn = confirm_user_choice()
        if useryn.lower() == "y":
            break
    display_value(Returncode)
    display_menu()
    UsersChoice = ask_user_for_task()