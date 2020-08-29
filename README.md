# Mars Project

## Background
The purpose of this project is to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

### Task
#### Step 1: Scraping
* Using Jupyter Notebook to web scrape the following information about Mars:
  * Scrape the latest News Title and Paragraph Text [here](https://mars.nasa.gov/news/).
  * Use Splinter to retrieve the current Mars image URL [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
  * Get the latest Mars tweet [here](https://twitter.com/marswxreport?lang=en).
  * Use Pandas to scrape the Mars Facts webpage [here](https://space-facts.com/mars/).
  * Collect all of the image URLs for each of Mars' hemispheres [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars).
  
#### Step 2: MongoDB and Flask Application
* Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
* Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements.

  
  


