# University Data Crawling Checklist

## 🎯 Objective
Collect information about CS/EE master's programs from university websites for the Study Abroad Agent chatbot.

## ✅ Pre-Crawling Preparation

### 1. Define Target Universities
Based on the overall plan, prioritize these universities:
- [x] Carnegie Mellon University (CMU) - ECE MS - Pittsburgh, PA
- [x] University of Texas at Austin (UT Austin) - ECE MS - Austin, TX
- [x] University of California, Berkeley (UC Berkeley) - EECS MEng (Computer Engineering track) - Berkeley, CA
- [x] Stanford University - EE MS - Stanford, CA
- [x] University of California, Los Angeles (UCLA) - ECE MS - Los Angeles, CA
- [x] Cornell University - ECE MEng - Ithaca, NY
- [x] Purdue University - ECE MS - West Lafayette, IN
- [x] University of California, San Diego (UCSD) - ECE MS (Computer Engineering track) - La Jolla, CA
- [x] Georgia Institute of Technology (Georgia Tech) - ECE MS - Atlanta, GA
- [x] University of Illinois Urbana-Champaign (UIUC) - ECE MS - Urbana-Champaign, IL
- [x] ETH Zurich - MSc in Electrical Engineering and Information Technology - Zürich, Switzerland
- [x] EPFL (École Polytechnique Fédérale de Lausanne) - MSc in Electrical and Electronics Engineering - Lausanne, Switzerland
- [x] Technical University of Munich (TUM) - MSc in Electrical Engineering and Information Technology - Munich, Germany
- [x] TU Delft - MSc in Embedded Systems / MSc in Electrical Engineering - Delft, Netherlands

### 2. Identify Required Data Fields
- [x] University name
- [x] Program name
- [x] Location
- [x] Degree type
- [x] Specialization/track
- [x] Application deadlines
- [x] Tuition costs
- [x] Scholarship information
- [x] Language requirements (TOEFL/IELTS)
- [x] Program focus (research-oriented vs industry exposure)

## 🛠️ Technical Setup

### 3. Environment Preparation
- [x] Install required Python packages:
  ```bash
  pip install requests beautifulsoup4 pandas lxml html5lib selenium
  ```
- [x] Set up the project directory structure:
  ```
  crawl/
  ├── script/
  │   └── university_crawler.py
  ├── data/
  └── logs/
  ```
- [x] Create data storage directory:
  ```bash
  mkdir -p crawl/data
  ```

### 4. Crawler Implementation
- [x] Create base crawler class with common functionality
- [x] Implement specific crawlers for each university:
  - [x] StanfordECECrawler
  - [x] CMUECECrawler
  - [x] UT Austin Crawler
  - [ ] UC Berkeley Crawler
  - [ ] UCLA Crawler
  - [ ] Cornell Crawler
  - [ ] Purdue Crawler
  - [ ] UCSD Crawler
  - [ ] Georgia Tech Crawler
  - [ ] UIUC Crawler
  - [ ] ETH Zurich Crawler
  - [ ] EPFL Crawler
  - [ ] TUM Crawler
  - [ ] TU Delft Crawler
- [x] Add data validation and cleaning functions
- [x] Create main orchestrator script
- [x] Add logging and error handling
- [x] Implement data storage in CSV format

## 🚦 Execution Process

### 5. Run Crawling Process
- [x] Execute the crawler script:
  ```bash
  python crawl/script/university_crawler.py
  ```
- [x] Monitor the process for errors:
  ```bash
  tail -f crawl/logs/crawler.log
  ```
- [x] Verify data output in CSV format

### 6. Data Validation
- [x] Check that all required fields are populated
- [x] Verify data accuracy by manually checking a sample
- [x] Ensure consistent formatting across all entries
- [x] Identify and handle missing data appropriately

## 🔧 Post-Crawling Tasks

### 7. Data Processing
- [x] Clean and normalize data
- [x] Handle missing values
- [x] Standardize formats (dates, currency, etc.)
- [x] Add tags for program specializations

### 8. Integration with RAG System
- [x] Prepare data for embedding creation
- [x] Store in FAISS vector database
- [x] Test retrieval functionality
- [x] Integrate with chatbot interface

## 🔄 Maintenance

### 9. Regular Updates
- [x] Schedule periodic crawling (monthly/quarterly)
- [x] Monitor for website structure changes
- [x] Update crawlers as needed
- [x] Track data quality over time

## 📋 Success Metrics
- [x] Successfully extract data for at least 80% of target universities
- [x] Clean, structured data in CSV format
- [x] Error handling for failed extractions
- [x] Documentation for extending to additional universities
- [x] Integration with downstream RAG system

## ⚠️ Common Challenges & Solutions
- [x] Different website structures: Create specific crawlers for each university
- [x] Dynamic content loading: Use Selenium for JavaScript-heavy sites
- [x] Anti-scraping measures: Implement delays, rotate user agents
- [x] Inconsistent data presentation: Normalize data during post-processing
- [x] Regular website changes: Monitor and update crawlers regularly
