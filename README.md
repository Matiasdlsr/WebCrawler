# Challenge-sirius

 ## NewsWebCrawler
 ### Task Overview
 This task involves developing a web crawler that generates concise summaries of
 newsarticles that users provide. The system will receive requests with news article
 URLs through a RESTendpoint that you need to develop. It will fetch these pages,
 extract the main content of the articles, and generate summaries. You can use
 any methodortool you prefer to perform the summarization.
 The initial source will only be articles from the BBC (https://www.bbc.com/news)

 
 ```Technical Details ```
 
 ● ```Scalability ```: You can assume that the load of the requests is about 1/sec, but
 makesurethat your design can support a load several orders of magnitude
 larger than that.
 
 ● ``` Otherproviders ```: The system should be able to escalate to other news
 providers easily (Clarin, La Nacion, etc). If the User inputs a URL that is not
 from a supported news provider, the system should respond with an error
 message that the provider has not yet been implemented.
 
 ● ``` URLHandling ```:URLsmightrepeatthemselves, and as with any good
 engineering system, we would like to avoid fetching and processing the
 samepageoverandoveragain.
 
 ● ```ContentExtraction```: News articles come from various websites with
 different HTML structures. Your system should reliably extract the main
 content of the article, excluding navigation menus, ads, comments, and
 other non-essential elements.
 
 ● ```TextProcessing```:
 ○ Summarization: Implementanefficient way to generate a concise
 summaryofthearticle's content. You can use any method or tool
 you prefer to perform the summarization.
 
 ● ```ErrorHandling```:
 ○ Ifthesite cannot access the news article because it requires an
 account or log in to view it, your service should return a custom error
 indicating that the article cannot be accessed.
 
● ```Performance Optimization```: Assume the corpus can be very large, so naive
 methods maynotbequickenoughtorenderresults promptly. You will
 need to address this through your choice of algorithms, data structures, or
 technologies.
 
 ● ```OutputFormat```:ThesummariesshouldbereturnedinaJSONformat. This
 is not a front-end development assignment, so you don't need to focus on
 making the output pretty.
 
 ● ```CachingandStorage ```: Implementcachingtostore processed articles to
 avoid redundant fetching and processing, thereby improving performance
 The list of URLs will be provided through a set of CURL calls. Please use
 simulateRequests.sh script to simulate those requests while you develop.
 
 For example, you can run it as follows:
 . /simulateRequests.sh localhost 8080 productUrl 1
