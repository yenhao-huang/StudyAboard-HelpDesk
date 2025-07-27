# University Data Crawler

This directory contains tools for crawling university program information for the Study Abroad Agent chatbot.

## 🎯 Purpose

Collect information about CS/EE master's programs from university websites to support the chatbot's recommendation system.

## 📁 Directory Structure

```
crawl/
├── script/                 # Crawling scripts
│   ├── university_crawler.py  # Main crawler implementation
│   └── run_crawler.sh     # Shell script to run the crawler
├── data/                   # Collected data (CSV format)
├── logs/                   # Crawler logs
├── docs/                   # Documentation
│   ├── university_crawl_plan.md   # Detailed crawling plan
│   └── university_crawl_checklist.md  # Execution checklist
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install requests beautifulsoup4 pandas lxml html5lib selenium
   ```

2. **Run the crawler using the shell script (recommended):**
   ```bash
   cd crawl/script
   ./run_crawler.sh
   ```

   Or run the Python script directly:
   ```bash
   python crawl/script/university_crawler.py
   ```

3. **Check the output:**
   The collected data will be saved to `crawl/data/university_programs.csv`
   Logs will be saved to `crawl/logs/crawler_YYYYMMDD_HHMMSS.log`

## 📊 Output Format

The crawler produces a CSV file with the following columns:

- `university`: Name of the university
- `program_name`: Name of the degree program
- `location`: University location (city, state/country)
- `degree_type`: Type of degree (MS, MEng, etc.)
- `track_focus`: Program specialization
- `application_deadline`: Application deadline information
- `tuition`: Tuition cost information
- `scholarship`: Scholarship/funding information
- `language_requirements`: Language test requirements (TOEFL/IELTS)
- `tags`: Keywords for program specializations

## 🛠️ Implementation Details

The crawler is implemented using:
- Python with requests and BeautifulSoup for web scraping
- Object-oriented design with a base crawler class
- Specific crawler implementations for each university
- CSV output for easy integration with the RAG system

## 📋 Checklist

See `docs/university_crawl_checklist.md` for a detailed checklist of the crawling process.

## 📈 Success Metrics

- Successfully extract data for all 14 target universities
- Clean, structured data in CSV format
- Error handling for failed extractions
- Documentation for extending to additional universities

## 🎯 Supported Universities

The crawler currently supports the following 14 universities:

1. Stanford University - EE MS
2. Carnegie Mellon University - ECE MS
3. University of Texas at Austin - ECE MS
4. University of California, Berkeley - EECS MEng (Computer Engineering track)
5. University of California, Los Angeles - ECE MS
6. Cornell University - ECE MEng
7. Purdue University - ECE MS
8. University of California, San Diego - ECE MS (Computer Engineering track)
9. Georgia Institute of Technology - ECE MS
10. University of Illinois Urbana-Champaign - ECE MS
11. ETH Zurich - MSc in Electrical Engineering and Information Technology
12. EPFL (École Polytechnique Fédérale de Lausanne) - MSc in Electrical and Electronics Engineering
13. Technical University of Munich - MSc in Electrical Engineering and Information Technology
14. TU Delft - MSc in Embedded Systems / MSc in Electrical Engineering

## ⚠️ Important Notes

- The crawler implements delays between requests to be respectful to university servers
- Some websites may require Selenium for dynamic content
- University websites change frequently, so crawlers may need periodic updates
- Always verify the accuracy of crawled data before using in production
