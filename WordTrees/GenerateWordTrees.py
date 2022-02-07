# This script was used to generate WordTrees.html interactive webpages for all 12 Optimized clusters for each Sample 1 and 2

# Import required libraries
import pandas as pd
import spacy
import random
nlp = spacy.load('en_core_web_sm')

# Load preprocessed data with numbers and some punctuation marks
df = pd.read_csv("PreProcessedDataWithNumbers.csv", usecols=[
                 "date", "id", 'title', 'clean_text'])


# Function to generate interactive WordTree webpages
def createWordTrees(sampNo=1):

    sentences = []

    def allSentences(x):

        doc = nlp(str(x))
        for sent in doc.sents:
            # print(sent.text)
            sentences.append(str(sent))

    sample = pd.read_csv(f"FinalLabelsSample{sampNo}.csv")

    temp = df.merge(sample, how='inner', left_on='id', right_on='ids')
    temp['date'] = pd.to_datetime(temp['date'])
    temp.set_index('date', inplace=True)
    print(len(temp))

    #clusterdf = temp[(temp.labels == 1) & (temp.index.month >= 5) & (temp.index.month <=10) & (temp.index.year == 2008)].copy()
    for i in range(1, 13):

        clusterdf = temp[temp.labels == i].copy()
        clusterdf['dummy'] = clusterdf['clean_text'].map(
            lambda x: allSentences(x))

        print(len(sentences))
        #sents = clusterdf['title'].to_list()

        # Shuffle the sentences twice thoroughly before using as an input in WordTree
        random.shuffle(sentences)
        random.shuffle(sentences)

        # Limiting the max number of sentences to 10,000 due to performance issues. Higher number of sentences take more memory and time to load and vice-versa
        sentences = sentences[:10000]

        sentsList = [[sent] for sent in sentences]
        use = str(sentsList)[1:-1]

        # HTML page with Javascript to enable interative web interface
        text = '''
        <html>
          <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
              google.charts.load('current', {packages:['wordtree']});
              google.charts.setOnLoadCallback(drawChart);

              function drawChart() {
                var data = google.visualization.arrayToDataTable(
                  [ ['Phrases'],
                    '''+use+''',
                  ]
                );

                // Select root word
                var root = document.getElementById('root').value || '';
                var chartType = document.querySelector('input[name = "type"]:checked').value || '';

                var options = {
                  wordtree: {
                    format: 'implicit',
                    type: chartType,
                    word: root
                  }
                };

                var chart = new google.visualization.WordTree(document.getElementById('wordtree_basic'));
                chart.draw(data, options);
              }

            </script>
          </head>
          <body>
            <p>
            <b><label for="root">Root word:&nbsp;</label></b>
            <input value="climate" id="root" />
            <input type="button" value="go" id="go" onClick="drawChart();" />
            &emsp;&emsp;
            <b><label for="type">Tree type:&nbsp;</label></b>
            <input type="radio" id="r1" name="type" value="double" checked="checked" onClick="drawChart();" /> Double
            <input type="radio" id="r2" name="type" value="suffix" onClick="drawChart();" /> Suffix
            <input type="radio" id="r3" name="type" value="prefix" onClick="drawChart();" /> Prefix

            <br><i>(try: "climate", "energy", "environment" etc.)</i>
            <div id="wordtree_basic" style="width: 1600px; height: 800px;"></div>
            </p>

            <script>
              var getInput = document.getElementById("root");

              getInput.addEventListener("keyup", function(event) {
                if (event.keyCode === 13) {
                  event.preventDefault();
                  document.getElementById("go").click();
                }
              });              
            </script>

          </body>
        </html>
        
        '''

        file = open(f"Sample{sampNo}Cluster{i}.html", "w")
        file.write(text)
        file.close()

        sentences = []


# Generate Word Trees for all 12 clusters for Sample 1 & 2
createWordTrees()
createWordTrees(sampNo=2)
