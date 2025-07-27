# University Data Crawling Solution

## Overview

This document describes the complete university data crawling solution implemented for the Study Abroad Agent chatbot. The solution collects information about CS/EE master's programs from university websites to support the chatbot's recommendation system.

## Components

### 1. Planning Documents
- `docs/university_crawl_plan.md`: Detailed plan for crawling university data
- `docs/university_crawl_checklist.md`: Execution checklist for the crawling process

### 2. Implementation
- `script/university_crawler.py`: Main Python script for crawling university data
- `script/run_crawler.sh`: Shell script to execute the crawler

### 3. Output
- `data/university_programs.csv`: Collected university program data in CSV format

## How It Works

### Data Structure
The crawler collects the following information for each university program:
- University name
- Program name
- Location
- Degree type
- Specialization/track
- Application deadlines
- Tuition costs
- Scholarship information
- Language requirements (TOEFL/IELTS)
- Program focus (research-oriented vs industry exposure)

### Technical Implementation
1. **Object-Oriented Design**: The crawler uses an abstract base class (`BaseUniversityCrawler`) with specific implementations for each university.
2. **Extensible Architecture**: New universities can be added by creating new crawler classes.
3. **Error Handling**: The orchestrator handles exceptions from individual crawlers.
4. **Respectful Crawling**: Implements delays between requests to avoid overloading servers.
5. **CSV Output**: Stores data in a structured format for easy integration with the RAG system.

### Current Implementation
The current implementation includes crawlers for:
- Stanford University - EE MS
- Carnegie Mellon University - ECE MS

Additional universities can be added by implementing new crawler classes following the same pattern.

## Usage

### Running the Crawler
1. Ensure dependencies are installed:
   ```bash
   pip install requests beautifulsoup4 pandas lxml html5lib selenium
   ```

2. Run the crawler using the shell script:
   ```bash
   cd crawl/script
   ./run_crawler.sh
   ```

3. Or run the Python script directly:
   ```bash
   cd crawl/script
   python university_crawler.py
   ```

### Output
The crawler produces a CSV file (`crawl/data/university_programs.csv`) with the collected data.

## Extending to Additional Universities

To add support for additional universities:

1. Create a new crawler class that inherits from `BaseUniversityCrawler`
2. Implement the `crawl()` method to extract data from the university website
3. Add the new crawler to the `crawlers` list in `UniversityCrawlerOrchestrator`
4. Test the new crawler

Example template for a new university crawler:
```python
class NewUniversityCrawler(BaseUniversityCrawler):
    def __init__(self):
        super().__init__(delay=1.0)
        self.university = "New University"
        self.program_name = "Program Name"
        self.location = "City, State/Country"
        self.degree_type = "MS"
        self.base_url = "https://example.edu/program"
    
    def crawl(self) -> List[UniversityProgram]:
        # Implementation to extract data from the university website
        # Return a list of UniversityProgram objects
        pass
```

## Integration with RAG System

The CSV output can be easily integrated with the existing RAG system:
1. The data can be processed to create embeddings
2. Embeddings can be stored in the FAISS vector database
3. The chatbot can retrieve relevant program information using semantic search
4. The RAG pipeline can use this information to generate responses to user queries

## Maintenance

To maintain the crawling solution:
1. Regularly check that university websites haven't changed their structure
2. Update crawler implementations as needed
3. Schedule periodic crawling to keep data current
4. Monitor for any anti-scraping measures that might block the crawler

## Future Enhancements

1. **Dynamic Content Handling**: Implement Selenium support for JavaScript-heavy websites
2. **Proxy Rotation**: Add proxy support to avoid IP blocking
3. **Rate Limiting**: Implement more sophisticated rate limiting
4. **Data Validation**: Add more comprehensive data validation and cleaning
5. **Incremental Updates**: Implement delta updates to avoid re-crawling all data
6. **Monitoring Dashboard**: Create a dashboard to monitor crawling status and data quality
