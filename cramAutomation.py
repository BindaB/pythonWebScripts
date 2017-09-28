import os, re, time, exceptions,sys,getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msvcrt import getch

def pyssword(prompt='Password: '):
    '''
        Prompt for a password and masks the input.
        Returns:
            the value entered by the user.
    '''

    if sys.stdin is not sys.__stdin__:
        pwd = getpass.getpass(prompt)
        return pwd
    else:
        pwd = ""        
        sys.stdout.write(prompt)
        sys.stdout.flush()        
        while True:
            key = ord(getch())
            if key == 13: #Return Key
                sys.stdout.write('\n')
                return pwd
                break
            if key == 8: #Backspace key
                if len(pwd) > 0:
                    # Erases previous character.
                    sys.stdout.write('\b' + ' ' + '\b')                
                    sys.stdout.flush()
                    pwd = pwd[:-1]                    
            else:
                # Masks user input.
                char = chr(key)
                sys.stdout.write('*')
                sys.stdout.flush()                
                pwd = pwd + char
                

###########################                  FUNCTIONS                  ##############################
#This function signs in to cram's website and brings up the relevant card deck
#username - the user's username
#password - the user's
#no return value
def signIn(username, password):
    #load webpage and put in login information
    driver.get('https://www.cram.com/user/login')
    try:
        usernameField = driver.find_element_by_id("username")
    except TimeoutException:
        print "Loading took too much time!"
    passwordField = driver.find_element_by_id("password")
    submit = driver.find_element_by_id('loginButton')
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    submit.click()
    #open card editing deck, get to last card and hit tab
    driver.get('http://www.cram.com/flashcards/edit/8074660')

    #check to see if there is a "already opened session" prompt
    try:
        driver.find_element_by_id('linkAddAnotherCard').click()
    except Exception:
        driver.find_element_by_xpath("//a[contains(@class,'as-continue allRounded greenBtn mediumBtn')]").click()    
        driver.find_element_by_id('linkAddAnotherCard').click()

#This function will         
#param i - i conjugation
#param youIS - you informal singular conjugation
#param he - he/she/it conjugation
#param we - we/you(formal)/they conjugation
#param youIP - you informal plural conjugation
#param englishWord - the english translation used for the front of a card
#no return value
def addVerb(i,youIS,he,we,youIP,englishWord):
    writeToCard("I " + englishWord,"ich " + i)
    writeToCard("you (informal singular) " + englishWord,"du " + youIS)
    writeToCard("he/she/it " + englishWord + "s", "er/sie/es " + he)
    writeToCard("we/you(formal)/they " + englishWord, "wir/Sie/sie " + we)
    writeToCard("you (informal plural) " + englishWord, "ihr " + youIP)


#This function will         
#param singleE - singular subject in english 
#param pluralE - plural subject in english
#param singleG - singlular subject in german
#param pluralG - plural subject in english
#param gender - gender of the noun in german
#no return value
def addWord(singleE, pluralE, singleG, pluralG,gender):
    if(gender.upper() == 'M'):
        gender = 'der'
    elif(gender.upper() == 'F'):
        gender = 'die'
    elif(gender.upper() == 'N'):
        gender = 'das'
    writeToCard("the " + singleE,gender + " " + singleG)
    writeToCard("the " + pluralE,gender + " " + pluralG)
    
#This function will write the front and back of a flashcard
#front - the contents of the front of a card
#back - the contents of the back of a card
#no return value
def writeToCard(front,back):
    driver.switch_to.active_element.send_keys(Keys.DELETE + Keys.BACKSPACE + front + Keys.TAB)
    driver.switch_to.active_element.send_keys(Keys.DELETE + Keys.BACKSPACE + back + Keys.TAB)
    
#######################            MAIN STARTS HERE          ########################
username = raw_input("username: ")
password = pyssword()
exit = 'N'

#get browser loaded
chromedriver = "/Users/bbinda/Desktop/chromedriver_win32/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

signIn(username,password)
addCard = driver.find_element_by_id('linkAddAnotherCard')
while(exit.upper() != "Y"):
    isVerb = raw_input("is this word a verb?: ").upper()
    englishWord = raw_input("english word: ")
    germanWord = raw_input("german word: ")
    #check to see if we're adding a verb or a subject
    if(isVerb.upper() == 'YES'):
        irregularVerb = raw_input("is the verb irregular (yes or no)?: ")
        #if irregular then prompt for input
        if(irregularVerb.upper() == "YES"):
            verbI = raw_input("I: ")
            verbYouIS = raw_input("you (informal singular): ")
            verbHe = raw_input("he/she/it: ")
            verbWe = raw_input("we/you(formal)/they: ")
            verbYouIP = raw_input("you (informal plural): ")
        #if regular verb then do traditional verb endings
        else:
            baseVerb = germanWord[0:-2]
            verbI = baseVerb + "e"
            verbYouIS = baseVerb + "st"
            verbHe = baseVerb + "t"
            verbWe = baseVerb + "en"
            verbYouIP = baseVerb + "t"

        addVerb(verbI,verbYouIS,verbHe,verbWe,verbYouIP,englishWord)
    else:
        englishWordPlural = raw_input("english plural: ")
        gender = raw_input("gender (m/f/n): ")
        wordSingle = raw_input("german single: ")
        wordPlural = raw_input("german plural: ")
        addWord(englishWord,englishWordPlural,wordSingle,wordPlural,gender)
    driver.switch_to.active_element
    exit = raw_input('done?(Y/N): ')
driver.quit()    
#######################            MAIN ENDS HERE          ########################
