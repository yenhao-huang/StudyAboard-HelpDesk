#!/bin/bash

# University Data Crawler Runner Script

# Exit on any error
set -e

# Print script info
echo "University Data Crawler"
echo "======================="
echo "Starting crawl process..."

# Create logs directory if it doesn't exist
mkdir -p ../logs

# Define log file
LOG_FILE="../logs/crawler_$(date +%Y%m%d_%H%M%S).log"

# Run the crawler script and redirect output to log file
echo "Running university crawler..."
echo "Logging to: $LOG_FILE"
python3 university_crawler.py > "$LOG_FILE" 2>&1

# Check if the output file was created
if [ -f "../data/university_programs.csv" ]; then
    echo "✅ Crawl completed successfully!"
    echo "📄 Output file: ../data/university_programs.csv"
    echo "📊 File size: $(ls -lh ../data/university_programs.csv | awk '{print $5}')"
    echo "📈 Row count: $(($(wc -l < ../data/university_programs.csv) - 1)) programs collected"
    echo "📝 Log file: $LOG_FILE"
else
    echo "❌ Crawl failed - output file not found!"
    echo "📝 Check log file: $LOG_FILE"
    exit 1
fi

echo "🏁 Crawl process finished."
