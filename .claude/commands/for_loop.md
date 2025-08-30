---
argument-hint: [list of cities]
description: gets the top news stories for each city
---

# algorithm

city_list = $ARGUMENT
output_list = [(source, headline, summary, hyperlink), ....]

for each city in city_list:
  1. lookup todays top news headline in that city
  2. fetch and read the article
  3. determine the url for the article
  4. summarize the article 
  5. add the [(source, headline, summary, hyperlink] to the output list

## lookup todays top news headline in that city

Assess top news based on the following criteria

Information: concrete details about the who, what, when, where and why. 
Significance: does this story have some significance, are many peoples lives going to be effected?
Form: Good news stories take shape and give the reader a sense of completion. As a public relations practitioner, you can help reporters generate form by offering a well-rounded set of facts and sources for a story. This list of facts and sources does not have to be formal, but should be comprehensive, focused and carefully coordinated.
Voice: Good stories also include good conversations. The reporter has a job to provide a narrative of facts and details; good, concise quotes will add color and accentuate points in the story. While reporters will likely want to obtain their own quotes for a story, including them in a pitch or news release, when relevant, can help to show a person’s personality and provide key insight that further inspires a reporter to pursue your story.

## determine the url for the article

the url should be the url for the actual article, not the url for the front page..

eg: https://www.indailysa.com.au/news/just-in/2025/08/29/thousands-without-power-as-wild-weather-batters-sa

and NOT

https://www.indailysa.com.au/

## summarize the article

With the notes you took as you read the article, write an outline that notes its main points and supporting arguments. This outline doesn’t need to be as detailed as an outline for an essay—it’s just a sketch you can use to make sure you cover all the necessary points when you write your summary.

Then determine the article’s main idea by identifying the central theme or argument the author presents and supports throughout the article. This typically appears near the beginning of the article, often in the introduction or early paragraphs. From here, determine any other “big picture” points the article makes and identify the details that support these points. Anything that isn’t a main idea or supporting argument can be left aside, as these aren’t important enough to be included in your summary.

A summary isn’t your opinion about the original article. To write an effective summary, keep your tone neutral and objective. Save your interpretations and analysis of the text for an analytical essay.

## output format

for each city produce output in Markdown as per below

not the double line breaks \n\n these are required due to the way claude-code handles markdown

  📍 [CITY_NAME] \n\n

  headline \n\n
  url \n\n
  summary \n\n
  source \n\n

for example

  📍 Berlin

  New displays for smooth bicycle traffic flow
  https://www.berlin.de/en/news/
  Berlin launched a pilot project introducing new display systems to help cyclists navigate traffic lights more efficiently, aiming to improve bicycle traffic flow throughout the city.
  Berlin.de

