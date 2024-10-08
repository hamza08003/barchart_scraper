# Currency Data Scraper

A Python-based web scraping project that collects currency indicator data from specified URLs and stores the information in a MySQL database. This project utilizes Selenium for web scraping and BeautifulSoup for HTML parsing, alongside a structured database to facilitate easy data management.

## Table of Contents

- [Working](#working)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)

## Working

- Scrapes currency data from predefined URLs.
- Supports scraping of multiple currency indicators.
- Stores scraped data in a MySQL database.
- Automatically maps currency names to their respective codes.
- Provides error handling for missing elements during scraping.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.x**: Download and install Python from [python.org](https://www.python.org/downloads/).
- **MySQL Server**: Install MySQL and set up a database. You can download MySQL from [mysql.com](https://dev.mysql.com/downloads/mysql/).
- **Google Chrome**: Ensure you have Google Chrome installed on your machine. Download it from [google.com/chrome](https://www.google.com/chrome/).
- **Necessary Python libraries**:
  - `selenium`
  - `beautifulsoup4`
  - `mysql-connector-python`
  - `pytz`
  - `schedule`
  
You can install the required libraries using pip:

```bash
pip install selenium beautifulsoup4 mysql-connector-python pytz schedule
```

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/currency-data-scraper.git
```

2. Navigate to the project directory:

```bash
cd currency-data-scraper
```

3. Create a JSON file named db_config.json in the project root to store your MySQL database credentials. The structure of the file should be as follows:

```json
{
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "database": "your_database_name"
}
```

4. Create a links.txt file in the project root containing the URLs you want to scrape, one per line.
 

## Usage

To run the scraper, execute the main script:

```bash
python scraper.py
```

## Database Structure

- `currency`: Holds currency names and their corresponding IDs.
- `ind_name`: Contains names of indicators and their IDs.
- `barchart_strength_direction`: Maps signal types (strength and direction) to their IDs.
- `barchart`: Stores scraped data including currency, indicator, strength, direction, signal type, and timestamps.
