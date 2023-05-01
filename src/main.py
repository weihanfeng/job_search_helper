from helper.get_job_openings import MCFScraper
from helper.get_top_similar import GetTopSimilar
from joblib import Parallel, delayed
from sample_resume import sample_resume
import pandas as pd


def main(job_title, max_page, conditions= None, top_k=1):
    # Get job opening details
    
    mcf_scraper = MCFScraper(
        job_title=job_title,
        main_url="https://www.mycareersfuture.gov.sg/search?search={}&sortBy=new_posting_date&page={}",
        base_post_url="https://www.mycareersfuture.gov.sg",
        conditions=conditions
    )
    job_urls = Parallel(n_jobs=-1)(
        delayed(mcf_scraper.get_job_urls)(page) for page in range(max_page)
    )
    job_urls = [item for sublist in job_urls for item in sublist if sublist]
    # Get job descriptions
    job_details = Parallel(n_jobs=-1)(
        delayed(mcf_scraper.get_job_details)(job) for job in job_urls
    )
    # Get job descriptions as list 
    job_descriptions = [job_info["description"] for job_info in job_details]
    # Convert to dataframe
    job_details = pd.DataFrame(job_details)

    print("Number of job listings obtained: ", len(job_details))

    # Get top similar
    get_top_similar = GetTopSimilar(strings=job_descriptions)
    results = get_top_similar.get_top_similar(query=sample_resume, k=top_k)
    results_docs = [result[0].page_content for result in results]

    # Get dataframe of rows with "description" in result_docs
    results_df = job_details[job_details["description"].isin(results_docs)]

    return results_df


if __name__ == "__main__":
    job_title = "geospatial data"
    max_page = 5
    conditions = ["entry level", "non-executive", "junior executive", "executive", "senior executive", "middle management", "senior management"]
    result_df = main(job_title, max_page, conditions=conditions, top_k=5)
    print(result_df)
    result_df.to_csv("top_jobs.csv", index=False)
