# HTML Text Coding Dashboard 

A lightweight, local, and fully customizable HTML dashboard for human annotation tasks designed for researchers conducting quantitative text analysis.

This tool takes your structured text data (e.g., news articles broken into chunks) and generates a single, standalone HTML file. Human annotators can open this file in any web browser, code the text, and export their results directly to a CSV file.

## Features
* **Zero Dependencies:** Generates a standalone HTML file. No server, database, or internet connection required for the coders.
* **Granular Coding:** Code documents at the chunk/paragraph level (radio buttons) and the document level (checkboxes).
* **Auto-Save:** Progress is saved locally in the browser. 
* **Built-in Codebook:** Embeds your PDF instructions directly into the dashboard, if preferred.
* **Instant Export:** One-click export to a perfectly formatted `.csv`.

## Included Example: News Valence
An example (`example_economynews.py`) tailored for coding news media valence is included in this repository to show how to configure inputs.

The example data utilizes short excerpts from the following news articles:
* **The Wall Street Journal:** *Paycheck Boost Gives Low-Income Workers a Breather* 
  [View Article](https://www.wsj.com/economy/jobs/paycheck-boost-gives-low-income-workers-a-breather-bfbd0313?mod=consumers_news_article_pos2)
* **The New York Times:** *American Small-Business Boom* 
  [View Article](https://www.nytimes.com/2026/07/17/business/economy/american-small-business-boom.html)

*Note: In the actual coding dashboard, human annotators are kept blind to the source outlet.*

## Quickstart

1. Clone the repository:
   ```bash
   git clone [https://github.com/zfrb/human-coding-dashboard.git](https://github.com/zfrb/human-coding-dashboard.git)
  ```
2. Run the example script to generate the HTML tool:
  ```bash
  python example_economy.py
  ```
3. Open the newly generated human_coding_economy_valence.html in any web browser and begin coding.
