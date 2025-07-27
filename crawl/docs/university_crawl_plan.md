# University Data Crawling Plan

## Objective
Create a web scraping solution to collect information about CS/EE master's programs from university websites for the Study Abroad Agent chatbot.

## Target Data
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

## Implementation Approach

### 1. University List
Based on the overall plan, we'll start with these universities:
- Carnegie Mellon University (CMU) - ECE MS - Pittsburgh, PA
- University of Texas at Austin (UT Austin) - ECE MS - Austin, TX
- University of California, Berkeley (UC Berkeley) - EECS MEng (Computer Engineering track) - Berkeley, CA
- Stanford University - EE MS - Stanford, CA
- University of California, Los Angeles (UCLA) - ECE MS - Los Angeles, CA
- Cornell University - ECE MEng - Ithaca, NY
- Purdue University - ECE MS - West Lafayette, IN
- University of California, San Diego (UCSD) - ECE MS (Computer Engineering track) - La Jolla, CA
- Georgia Institute of Technology (Georgia Tech) - ECE MS - Atlanta, GA
- University of Illinois Urbana-Champaign (UIUC) - ECE MS - Urbana-Champaign, IL
- ETH Zurich - MSc in Electrical Engineering and Information Technology - Zürich, Switzerland
- EPFL (École Polytechnique Fédérale de Lausanne) - MSc in Electrical and Electronics Engineering - Lausanne, Switzerland
- Technical University of Munich (TUM) - MSc in Electrical Engineering and Information Technology - Munich, Germany
- TU Delft - MSc in Embedded Systems / MSc in Electrical Engineering - Delft, Netherlands

### 2. Technical Implementation
- Use Python with requests and BeautifulSoup for static content scraping
- Use Selenium for dynamic content (if needed)
- Store data in CSV format for easy integration with the existing system
- Implement error handling and retry mechanisms
- Add rate limiting to respect website servers

### 3. Data Structure
```csv
university,program_name,location,degree_type,track_focus,application_deadline,tuition,scholarship,language_requirements,tags
```

### 4. Implementation Steps
1. Create a base crawler class with common functionality
2. Implement specific crawlers for each university (as URL structures vary)
3. Add data validation and cleaning functions
4. Create a main orchestrator script
5. Add logging and error handling
6. Implement data storage in CSV format

## Expected Challenges
- Different website structures for each university
- Dynamic content loading requiring Selenium
- Anti-scraping measures (CAPTCHAs, IP blocking)
- Inconsistent data presentation across websites
- Regular changes to website layouts

## Success Criteria
- Successfully extract data for at least 80% of target universities
- Clean, structured data in CSV format
- Error handling for failed extractions
- Documentation for extending to additional universities
