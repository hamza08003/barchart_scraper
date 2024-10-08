# Currency Data Scraper

A Python-based web scraping project that collects currency indicator data from specified URLs and stores the information in a MySQL database. This project utilizes Selenium for web scraping and BeautifulSoup for HTML parsing, alongside a structured database to facilitate easy data management.

## Table of Contents

- [Working](#working)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Scheduled Execution](#scheduled-execution)
- [License](#license)

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
