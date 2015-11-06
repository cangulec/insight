#!/usr/bin/env bash
chmod +x src/tweets_cleaned.py;
chmod +x src/average_degree.py;
python src/tweets_cleaned.py tweet_input/tweets.txt tweet_output/ft1.txt
python src/average_degree.py tweet_input/tweets.txt tweet_output/ft2.txt
if which sfdp >/dev/null; then
    echo "Graphviz is installed"
    echo "Generating graph.png..."
    sfdp -Tpng tweet_output/graphviz.txt -o tweet_output/graph.png -Gcharset=latin1
else
    echo "Need to install Graphviz for visualization"
    sudo pip install graphviz
    sfdp -Tpng tweet_output/graphviz.txt -o tweet_output/graph.png -Gcharset=latin1
fi
