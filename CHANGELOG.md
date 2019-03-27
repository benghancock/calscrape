# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-dev] - 2019-03-25
### Interface changes
- user input is handled via command line arguments using `argparse`, not
  interactive
- search modes include `full` (scrape all hearing data), `silent` (save all
  data as JSON file), and `keyword` (regex match for keyword arg, matching
  results printed to stdout). 
- deprecated search functionality for list of terms (deleted `user/` dir)
- scrape time takes longer due to introduction of `sleep` in `calendar_parser`
  module; done to avoid heavy load on court servers

### Refactoring changes
- deprecated `calparse` and `spatula` modules; moved calendar parsing into
  `calendar_parser` using new `CalendarParser` class 
- scraping no longer relies on JSON file containing individual URLs for court
  calendars; URLs are pulled dynamically from court index page (deleted `data` dir) 
