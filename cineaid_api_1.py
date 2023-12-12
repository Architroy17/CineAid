#created by archit roy

#python api to take web browser tab title and return information about it 
#**** below might mention movie_title several times but this code works for tv series too***#


#uvicorn cineaid_api_1:app to run on localhost

from fastapi import FastAPI #to create api
import requests #to make http requests 
from bs4 import BeautifulSoup #to webscrape html
from lxml import etree #process html using xpath
import re #regex matching for filtering tab title


#function to extract movie_title from tab title
def extract_movie_title(input_string):
    # Define regular expressions for each type
    # Extracts the movie title from different input formats
    # Args: input_string (str): The input string containing information about the movie.
    # Returns:str or None: The extracted movie title if a match is found, otherwise None.

    patterns = [
        re.compile(r'^Prime Video: (.+)$'), #Prime Video: movie_title
        re.compile(r'^(.+) - Disney\+ Hotstar$'), #movie_title - Disney+ Hotstar
        re.compile(r'^(.+) - Netflix$'), #movie_title - Netflix
        re.compile(r'^(.+) Watch Full Movie Online - Fmovies(free)?$'), #movie_title Watch Full Movie Online - Fmovies(free)
    ]

    # Check each pattern and return the extracted title if a match is found
    for pattern in patterns:
        match = pattern.match(input_string)
        if match:
            return match.group(1).strip()

    # Return None if no match is found
    return None



#generate url for bing to get ratings, director
def generate_bing_url(movie_title):
    # remove any leading or trailing whitespaces
    movie_title = movie_title.strip()
    # replace all spaces with '+'
    movie_title_with_addition = '+'.join(movie_title.split())
    # generate the URL string
    url = f"https://www.bing.com/search?pglt=41&q={movie_title_with_addition}+rating&FORM=ANNTA1&PC=ASTS"
    return url



#generate url for bing to get cast
def generate_bingcast_url(movie_title):
    # remove any leading or trailing whitespaces
    movie_title = movie_title.strip()
    # replace all spaces with '+'
    movie_title_with_addition = '+'.join(movie_title.split())
    # generate the URL string
    url = f"https://www.bing.com/search?pglt=41&q={movie_title_with_addition}+cast&FORM=ANNTA1&PC=ASTS"
    return url



#generate url for bing to get smiliar movies
def generate_bingsimilar_url(movie_title):
    # remove any leading or trailing whitespaces
    movie_title = movie_title.strip()
    # replace all spaces with '+'
    movie_title_with_addition = '+'.join(movie_title.split())
    # generate the URL string
    url = f"https://www.bing.com/search?pglt=41&q={movie_title_with_addition}+similar&FORM=ANNTA1&PC=ASTS"
    return url


#generate url for rotten to get critic reviews
def generate_rotten_url(movie_title):
    # remove any leading or trailing whitespaces
    movie_title = movie_title.strip()
    # replace all spaces with underscores
    movie_title_with_underscore = '_'.join(movie_title.split())
    # generate the URL string
    url = f"https://www.rottentomatoes.com/m/{movie_title_with_underscore}/reviews"
    return url



app = FastAPI()

@app.get("/movie_info/{movie_title}")
def movie_info(movie_title: str):
    # Extract movie title using the previously defined function
    extracted_title = extract_movie_title(movie_title)

    # Check if title extraction was successful
    if not extracted_title:
        return {'error': 'Failed to extract movie title'}

    retries = 0

    while retries < 6:
        try: #
            # Use the extracted title in the URL generation functions
            bing_url = generate_bing_url(extracted_title)
            rotten_url = generate_rotten_url(extracted_title)
            bingcast_url = generate_bingcast_url(extracted_title)
            bingsimilar_url = generate_bingsimilar_url(extracted_title)

            # Rest of the code remains unchanged
            # Set the user-agent for the HTTP request headers
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            # Make an HTTP GET request to the URL for movie cast information
            r = requests.get(bingcast_url, headers=headers)
            # Parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(r.content, 'html.parser')
            # Create an HTML DOM tree using lxml
            dom = etree.HTML(str(soup))
            # Extract movie cast information using XPath
            cast = dom.xpath("//div[@class='tit']/strong/text()") #get CAST
            #SAME FOR BELOW CODES


            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            r = requests.get(bingsimilar_url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            dom = etree.HTML(str(soup))
            similar = dom.xpath("//div[@class='tit']/strong/text()") #get SIMILAR


            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            r = requests.get(bing_url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            dom = etree.HTML(str(soup))
            rating = dom.xpath("//div[@class='l_ecrd_ratings_prim']/text()") #get RATING
            director = dom.xpath("//div[@class='lc_expfact_default']/a[2]/text()") #get DIRECTOR


            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            r = requests.get(rotten_url, headers=headers)
            soup = BeautifulSoup(r.content,'html.parser')
            dom = etree.HTML(str(soup))
            review = dom.xpath("//div[@class='review-text-container']/p[@class='review-text']/text()") #get REVIEWS
            geanre = dom.xpath("//ul[@data-qa='sidebar-movie-details']/li[2]/text()") #get GEANRE BUT WITH WHITESPACE,NEWLINE ETC
            cleaned_genare = geanre[0].strip() if geanre else "" # Extract genre information from the list, and clean it if it exists
            cleaned_genare = cleaned_genare.replace('\n', '') if cleaned_genare else "" # Remove newline characters from the cleaned genre string, if it exists
            f_geanre = cleaned_genare #FILTERED_GEANRE


            return {
                'title': extracted_title,
                'ratings': rating,
                'geanre': f_geanre,
                'director': director[0] if director else "",
                'cast': cast[:5] if cast else [],
                'review': review[:3] if review else [],
                'similar': similar[::2] if similar else []
            }
        except Exception as e: #TILL 6TH FAILED TRY
            retries += 1
            print(f"Error occurred in attempt {retries}: {str(e)}")
    
    return {
        'title': extracted_title,
        'ratings': [],
        'geanre': f_geanre,
        'director': director,
        'cast': [],
        'review': [],
        'similar': []
    }# Return a dictionary with default values in case of unsuccessful data




#http://127.0.0.1:8000/movie_info/Prime Video: Predestination   sample link to api


# sample output:

# {"title":"Predestination",
#  "ratings":["7.4/10","84%","69/100"],
#  "geanre":"Sci-Fi,Action,Mystery & Thriller",
#  "director":"Michael Spierig",
#  "cast":["Ethan Hawke","Sarah Snook","Noah Taylor","Madeleine West","Christopher Kirby"],
#  "review":["It’s a fascinating investigation into the major science-fiction theme of time 
#            travel and the sometimes mindbending possibilities therein.","This twisting, turning,
#            time-travelling thriller about the ability to change the course of destiny will leave
#            you pondering long after the credits have rolled.","Challenges the ultimate impossibility
#            with themes of existence, procreation, choices, destiny, and whether the end justifies 
#            the means...a 360-degree head scratcher. And the word \"360-degree\" will have a new meaning
#            when you realize the full story."],
#  "similar":["Daybreakers","Coherence","Jessabelle","The Guest","The Maze Runner",
#             "Housebound","Nightcrawler","Boyhood","Time Lapse","Stonehearst Asylum"]
# }