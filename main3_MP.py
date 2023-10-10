import requests
import os
import pandas as pd
from multiprocessing import Process

folder_path = 'papers/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


def download_pdf(doi):
    base_url = "https://sci-hub.live/"
    
    # Construct the URL for the PDF download
    url = base_url + doi

    # Send a GET request to the URL
    response = requests.get(url)


    #print(response.content)

    if response.status_code == 200:
        # Extract the download URL from the search response
        x = response.text.find('ion/pdf" src="')
        if x == -1:
            print("Can not find the paper")
            return
            
        x = x+16
        t = response.text.find('#', x,x+200)
        download_url = response.text[x:t]
        if download_url[:5] == 'ownlo':
            download_url = base_url+'d'+download_url
        else:
            download_url = 'https://'+ download_url
        print(download_url)
    else:
        print("Can not get Download url")
    
    
    file_name = doi.replace('/', '_')
    
    # Check if the request was successful
    try:
        pdf_response = requests.get(download_url)
        with open(os.path.join(folder_path, f"{file_name}.pdf"), "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"PDF downloaded successfully: {file_name}.pdf")
    except Exception as e:
        print(f"Error downloading PDF: {e}")

def process_doi(doi):
    print(f"Processing DOI: {doi}")
    download_pdf(doi)

if __name__ == '__main__':
    df = pd.read_csv('Exported Items.csv')
    saved_column = df['DOI']

    # Create a separate process for each DOI
    processes = []
    for item in saved_column:
        p = Process(target=process_doi, args=(item,))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("All downloads completed.")

