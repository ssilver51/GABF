# Background
The Great American Beer Festival (shortened to GABF) is an annual beer festival/competition held in Denver, Colorado. The event was founded in 1982 in Boulder, CO and has grown to become the largest ticketed beer competition in the United States. In recent years the event has been held in the Colorado Convention Center, with as many as **800** participating breweries and **62,000** attendees (2018).
<br><br>
The competition chooses winners by awarding bronze, silver, and gold medals for each beer category. GABF defines the critera for these medals as:
| Award  	| Description                                                                                                                                                         	|
|--------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Gold   	| A world-class beer that accurately exemplifies the specified style, displaying the proper balance of taste, aroma and appearance.                                   	|
| Silver 	| An excellent beer that may vary slightly from style parameters while maintaining close adherence to the style and displaying excellent taste, aroma and appearance. 	|
| Bronze 	| A fine example of the style that may vary slightly from style parameters and/or have minor deviations in taste, aroma or appearance.                                	|

# Data
GABF has published all of their award winners on [their website](https://www.greatamericanbeerfestival.com/the-competition/winners/). Although this data is formatted in an HTML table, I was not able to find a direct download. To begin exploring this data, I scraped the linked website using a combination of Selenium (to interact with JavaScript elements) and BeautifulSoup (to parse the HTML).
<br>

The dataset contained 6047 award winners, spanning the years of 1983-2019.
<br>
| Field     	| Description                                                  	|
|-----------	|--------------------------------------------------------------	|
| Medal     	| The award received (Gold, Silver, Bronze, Honorable Mention) 	|
| Beer Name 	| Name of the award-winning beer                               	|
| Brewery   	| Name of the award-winning brewery                            	|
| City      	| City of the brewery                                          	|
| State     	| State in which the brewery operates                          	|
| Category  	| Beer category the award was given                            	|
| Year      	| Year the award was won                                       	|

# Exploratory Data Analysis
## Growth of the Competition
When examining time-series data related to the competition, an obvious trend is observed. Since its inception in 1983, the competition has significantly grown in participants, medals awarded, attendees, etc.
<br>
<br>
<img src="images/count_winners_over_time.png" width=800 align=center>
<br>
<br>
This makes sense, as the competition has grown, more medals get awarded. Since medals are awarded by category, if the number of medals awarded has increased, we would expect the same trend in the number of categories.
<br>
<br>
<img src="images/count_cats_over_time.png" width=800 align=center>
<br>
<br>
What about the number of participants? Does the Great American Beer Festival have representatives from every state?
<br>
<br>
<img src="images/count_states_over_time.png" width=800 align=center>
<br>
<br>
Interesting! Although GABF has had entries from all 50 states over the lifetime of the event, it appears no specific year has had more than 40 states represented.


## Who Wins the Most?
We have established that the competition has had a near-linear growth in winners and categories, but who tends to bring home the medals? We can look at quite a few data points to answer that.

### Breweries
Which breweries have the most medals on their wall?
<br>
<br>
<img src="images/brewery_medals.png" width=800 align=center>
<br>
<br>
We see some **very** familiar names on this list. The top three: Pabst, Anheuser Busch, and Miller are some of the largest and oldest brewing companies in the country. Although they hardly meet the definition of "craft" breweries, it makes sense they'd be so well represented simply due to their age.
<br>
<br>
That is all fine and well, but let's look a bit more granular. Let's take a look at the medal-breakdown for these same breweries.
<br>
<br>
<img src="images/brewery_medals_clustered.png" width=800 align=center>
<br>
<br>
Some interesting data points here. Firstly, we can observe that out of 72 total medals won by Pabst, only 13 of those have been bronze (~18%). A clear breakout is Boston Beer Co., out of their 42 total medals, 23 of them are gold (~55%).

### States
Which states tend to bring home medals?
<br>
<br>
<img src="images/state_medals.png" width=800 align=center>
<br>
<br>
It seems like California and Colorado have the highest representation as far as medals are concerned. This makes sense, as CA and CO are both considered ahead-of-the-curve when it comes to craft beer, in fact the [Brewer's Association](https://www.brewersassociation.org/statistics-and-data/state-craft-beer-stats/) ranks California and Colorado first and second in terms of number of breweries in the country.
<br>
<br>
Nothing too surprising here, let's look at the medal breakdown for these states.
<br>
<br>
<img src="images/state_medals_clustered.png" width=800 align=center>
<br>
<br>
The data looks pretty similar, but we can observe that when CA and CO win, they seem to win more silver than gold. If we look at states like TX and WA, we can see that when breweries from their states win, they appear to win gold a bit more often; but not by much. Overall it seems like these states have a generally equal likelihood of winning gold, silver, or bronze.

### Cities
Which cities are best represented?
<br>
<br>
<img src="images/city_medals.png" width=800 align=center>
<br>
<br>
First thing I notice is that California doesn't have nearly the same represention when we break down winners by city. Why would this be the case? Perhaps because California's population is spread out over a larger area, they have fewer cities with high concentrations of winners. Even still, I'd expect to see more than one city in CA on this list!
<br>
<br>
A second interesting fact about this data, four out of the top fifteen winning cities are in Colorado! That is surprising, as I'd certainly expect cities like Golden to be less represented than a huge city like Boston. Perhaps this is simply due to the fact that the competition is held in CO, so CO breweries are more likely to enter. Even though GABF is the largest beer festival/competition in the country, it makes sense that tiny breweries in the state of MA are less likely to enter than similarly-sized breweries in the home-state of the competition.
<br>
<br>
Also interesting to see that Salt Lake City, Utah has the 10th most medals out of any city, but Utah wasn't even in the top 15 of medal-winning states.
<br>
<br>
Again, let's break it down by medal:
<br>
<br>
<img src="images/city_medals_clustered.png" width=800 align=center>
<br>
<br>
Whoa! There are a lot more discrepencies between medals than when we looked state-wide. Although Denver seems to win similar number of gold, silver, and bronze medals; cities like Boston, MA (thanks Boston Beer Co. for ~80% of those gold medals); Austin, TX; and Fort Collins, CO have won *many* more gold medals than silver or bronze. When they win, they seem to win big!
<br>
<br>
Looking at total medals, Denver is winning by a pretty solid margin, but if we just look at **gold** medals, we have a pretty close race! Portland, OR is only 9 gold medals behind us (compared to nearly 50 total medals). We can also see that Seattle, WA is actually 3rd in gold medal wins (compared to 4th in total medal wins); with Milwaukee, WI falling back nearly four places.
<br>
<br>
### Map Over Time
What does this data look like over time?
<br>
<img src="images/map_animation.gif" width=800 align=center>
<br>
<br>
We see some familiar hotspots! Big concentration of wins in Denver, but also other cities in CO such such as Boulder, Fort Collins, and Golden seem to make our state look like quite the beer hub! California also seems to have quite the representation, with nearly half the state covered in points by 2019.
<br>
<br>
We can also recognize some of our other breakout cities on this chart; such as Portland, Seattle, Austin, and Chicago.
<br>
<br>
One surprise brought to light by this chart is the all of the wins along the east coast. Although you wouldn't have guessed by looking at our Top 15 bar charts, the entire east coast turns into a slurry of dots by 2019, making it nearly impossible to even discern the states! Compared to middle America, the east coast has a serious concentration of good beer!

## Beer Names
Let's take a look at the names of these award-winning beers and see if we notice any trends.
<br>
<br>
<img src="images/word_cloud_beer_names.png" width=800 align=center>
<br>
<br>
Well, this isn't all that interesting. We see "Ale", "Pale Ale", "Stout", "Lager" are some of the biggest words on this word cloud. This is not that surprising, as those are all very popular *categories* for the competition. 
<br>
<br>
If we had to take something away from this chart, it is to include the style of your beer in it's name!
<br>
<br>
Let's take a crack at removing some of these category keywords from our word cloud. While we are at it, let's remove some of the brewery names as well.
<br>
<br>
<img src="images/word_cloud_beer_names_without_brewery_or_category_keywords.png" width=800 align=center>
<br>
<br>
That is a bit better. We got rid of the official category names from our word cloud, but we still have a few stragglers like "IPA", "Pils", and "Barleywine". After some investigation, I found that although these are commonly known beer styles, they are not the **official** names used in GABF categories (for example, GABF uses the full name "India Pale Ale" rather than "IPA").
<br>
<br>
Even so, we can take a few inferences from this word cloud. We see a few descriptive words that appear quite frequently, such as "Cherry", "Milk", "Bourbon", "Gold", and "Apricot". It appears adjectives such as these have a positive impact on how well a beer is recieved. 
<br>
<br>
Perhaps these adjectives have a positive impact because it allows one to get some insight to what they are about to drink, rather than be surprised by an nondescript name.
<br>
<br>
For example, if you plan on premiering your new apricot-infused gold lager at the Great American Beer Festival, it appears the best name for it should contain the keywords "Apricot", "Gold", and "Lager".

# Analysis
After exhaustive exploration of all this data, it seems reasonable to ask: **Are GABF-medal-awarded beers any better than other beers?**
<br>
<br>
To answer this, I pulled in a dataset from [Kaggle](https://www.kaggle.com/rdoume/beerreviews) containing **1,672,016** beer reviews pulled from a review website called [BeerAdvocate](https://www.beeradvocate.com/).
<br>
<br>
This dataset contained beer names, brewery names, and a few review scores rated 1-5. Let's explore one score in particular, the **overall score**.
<br>
<br>
After some cleaning and fuzzy matching, I was able to split this dataset into two samples; one sample contained 171,529 reviews, all specific to beers that have recieved a GABF medal, and the other sample contained 1,500,487 reviews, all specific to beers that have NOT won a medal at the Great American Beer Festival.
<br>
<br>

$\cos$

# Sources

https://www.greatamericanbeerfestival.com/the-competition/about-the-beer-competition/
<br>
https://www.greatamericanbeerfestival.com/info/faq/
<br>
http://www.nbcnews.com/id/44430953
<br>
https://www.brewersassociation.org/statistics-and-data/state-craft-beer-stats/
<br>
https://www.kaggle.com/rdoume/beerreviews
<br>
https://www.beeradvocate.com/