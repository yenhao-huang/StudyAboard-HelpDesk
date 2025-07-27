# Extending the University Crawler

This guide explains how to add support for additional universities to the university crawler.

## Prerequisites

Before extending the crawler, ensure you have:
1. Python 3.6+
2. Required packages installed:
   ```bash
   pip install requests beautifulsoup4 pandas lxml html5lib selenium
   ```

## Adding a New University

### 1. Analyze the University Website

First, examine the university's website to identify:
- URLs for program information
- Structure of the HTML content
- Location of relevant data (deadlines, tuition, etc.)

### 2. Create a New Crawler Class

Create a new class that inherits from `BaseUniversityCrawler` in `crawl/script/university_crawler.py`:

```python
class NewUniversityCrawler(BaseUniversityCrawler):
    def __init__(self):
        super().__init__(delay=1.0)
        self.university = "New University Name"
        self.program_name = "Program Name"
        self.location = "City, State/Country"
        self.degree_type = "MS"  # or "MEng", "MSc", etc.
        self.base_url = "https://example.edu/program-url"
    
    def crawl(self) -> List[UniversityProgram]:
        """Crawl university program information."""
        logger.info(f"Crawling {self.university} - {self.program_name}")
        
        # Fetch the webpage
        soup = self._get_page(self.base_url)
        if not soup:
            return []
        
        # Extract data from the page
        # This is where you'll implement the specific logic for this university
        # Example:
        # deadline = soup.find('div', class_='deadline').text.strip()
        # tuition = soup.find('div', class_='tuition').text.strip()
        
        program = UniversityProgram(
            university=self.university,
            program_name=self.program_name,
            location=self.location,
            degree_type=self.degree_type,
            track_focus="research-oriented",  # or "industry exposure"
            application_deadline="December 15",  # Extracted from website
            tuition="$XX,XXX per year",  # Extracted from website
            scholarship="Yes, departmental funding available",  # Extracted from website
            language_requirements="TOEFL 100 or IELTS 7.0",  # Extracted from website
            tags="computer architecture, embedded systems"  # Relevant keywords
        )
        
        return [program]
```

### 3. Add the New Crawler to the Orchestrator

Add your new crawler to the list in the `UniversityCrawlerOrchestrator` class:

```python
class UniversityCrawlerOrchestrator:
    def __init__(self):
        self.crawlers = [
            StanfordECECrawler(),
            CMUECECrawler(),
            NewUniversityCrawler()  # Add your new crawler here
            # Add more crawlers here for other universities
        ]
```

### 4. Test Your New Crawler

Run the crawler to test your new implementation:

```bash
cd crawl/script
./run_crawler.sh
```

Check the output file to ensure your data was collected correctly:
```bash
cat ../data/university_programs.csv
```

## Best Practices

### 1. Respect Website Resources
- Always implement delays between requests
- Check `robots.txt` file for crawling permissions
- Don't overload servers with too many requests

### 2. Handle Errors Gracefully
- Use try/except blocks for parsing operations
- Return empty lists when data can't be extracted
- Log errors for debugging

### 3. Data Quality
- Validate extracted data
- Handle missing information appropriately
- Maintain consistent formatting

### 4. Code Structure
- Follow the existing code patterns
- Use descriptive variable names
- Add comments for complex parsing logic

## Example Implementation

Here's a more complete example for a hypothetical university:

```python
class MITComputerScienceCrawler(BaseUniversityCrawler):
    def __init__(self):
        super().__init__(delay=1.5)  # Slightly longer delay
        self.university = "Massachusetts Institute of Technology"
        self.program_name = "Master of Engineering in Computer Science"
        self.location = "Cambridge, MA"
        self.degree_type = "MEng"
        self.base_url = "https://www.eecs.mit.edu/academics/graduate-programs"
        self.deadline_url = "https://gradadmissions.mit.edu/apply/deadlines"
    
    def crawl(self) -> List[UniversityProgram]:
        """Crawl MIT Computer Science program information."""
        logger.info(f"Crawling {self.university} - {self.program_name}")
        
        # Get main program page
        soup = self._get_page(self.base_url)
        if not soup:
            return []
        
        # Get deadlines page
        deadline_soup = self._get_page(self.deadline_url)
        if not deadline_soup:
            return []
        
        # Extract program focus (this would be from the main page)
        track_focus = "research-oriented"
        
        # Extract deadline (this would be from the deadlines page)
        # This is a simplified example - real implementation would be more robust
        deadline_element = deadline_soup.find('td', string='MEng Computer Science')
        if deadline_element:
            application_deadline = deadline_element.find_next('td').text.strip()
        else:
            application_deadline = "Check website for deadlines"
        
        # Extract tuition information
        tuition_element = soup.find('h3', string='Tuition and Fees')
        if tuition_element:
            tuition = tuition_element.find_next('p').text.strip()
        else:
            tuition = "Check website for current tuition"
        
        program = UniversityProgram(
            university=self.university,
            program_name=self.program_name,
            location=self.location,
            degree_type=self.degree_type,
            track_focus=track_focus,
            application_deadline=application_deadline,
            tuition=tuition,
            scholarship="Limited departmental funding available",
            language_requirements="TOEFL 90 or IELTS 7.0",
            tags="computer science, artificial intelligence, machine learning"
        )
        
        return [program]
```

## Troubleshooting

### Common Issues

1. **403 Forbidden Errors**: The website may be blocking requests. Try:
   - Adding more headers to mimic a real browser
   - Using a proxy
   - Checking if the site requires authentication

2. **Missing Data**: Elements may not be found on the page. Try:
   - Checking if the page loads content dynamically with JavaScript
   - Using Selenium for JavaScript-heavy sites
   - Looking for alternative selectors

3. **Data Format Issues**: Data may not be in the expected format. Try:
   - Adding data cleaning and validation
   - Using regular expressions to extract specific patterns
   - Handling different date formats

### Debugging Tips

1. Print the HTML content to see what's actually being fetched:
   ```python
   print(soup.prettify())
   ```

2. Use browser developer tools to inspect elements and find selectors

3. Test selectors in a Python shell:
   ```python
   element = soup.find('div', class_='deadline')
   print(element.text if element else "Not found")
   ```

## Questions?

For questions about extending the crawler, refer to:
- `docs/university_crawl_plan.md` for overall strategy
- `docs/university_crawl_checklist.md` for implementation steps
- Existing crawler implementations as examples
