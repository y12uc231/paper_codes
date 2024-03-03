import requests
from urllib.parse import quote
import argparse

def get_dblp_bib_citation(paper_title):
    # URL encode the paper title to handle spaces and special characters
    encoded_title = quote(paper_title)
    
    # Construct the search URL for DBLP
    search_url = f"https://dblp.org/search/publ/api?q={encoded_title}&format=json"
    
    # Send a request to the DBLP API
    response = requests.get(search_url)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        try:
            # Extract the first hit's URL for the publication
            pub_url = data['result']['hits']['hit'][0]['info']['url']
            
            # The BibTeX URL is usually the publication URL with ".bib" at the end
            bib_url = pub_url + ".bib"
            
            # Fetch the BibTeX citation
            bib_response = requests.get(bib_url)
            
            if bib_response.status_code == 200:
                return bib_response.text
            else:
                return "Failed to fetch BibTeX citation."
        except (KeyError, IndexError):
            return "Publication not found."
    else:
        return "Failed to search DBLP."

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Fetch BibTeX citation for a paper from DBLP.')
    # Add an argument for the paper title
    parser.add_argument('paper_title', type=str, help='The title of the paper to search for.')
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Get the BibTeX citation
    bib_citation = get_dblp_bib_citation(args.paper_title)
    print(bib_citation)

if __name__ == '__main__':
    main()

