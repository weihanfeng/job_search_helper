class GetJobOpenings:
    """Scrape job openings from a website"""
    
    def __init__(self, website, query, num_results):
        self.website = website
        self.query = query
        self.num_results = num_results
    
    def get_job_openings(self):
        if self.website == "mcf":
            return self._get_job_openings_mcf()
    
    def _get_job_openings_mcf(self):
        pass