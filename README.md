# CineAid

CineAid is an chrome extension designed to enhance your browsing experience by providing comprehensive information about movies and TV series directly from your browser's active tab. The project consists of a Chrome extension and a FastAPI backend, offering a seamless and efficient way to access details such as ratings, genre, director, cast, reviews, and similar titles to help you decide if you want to watch it or not.

Screenshots on the extension being used displaying all the information about the movie/tv series opened.

Prime Video:
![prime_video_demo](https://github.com/Architroy17/CineAid/assets/91129894/d67b172a-47f1-4af5-83cd-a57ba28c5b96)
Netflix:
![netflix_demo](https://github.com/Architroy17/CineAid/assets/91129894/9d66031d-7ace-43e5-ab36-43d5b1ef0af8)
Hotstar:
![hotstar_demo](https://github.com/Architroy17/CineAid/assets/91129894/111e613d-cfeb-4f46-96c4-7ae0e8364834)
Fmovies:
![fmovies_demo](https://github.com/Architroy17/CineAid/assets/91129894/daafe0cc-2f1b-416f-a8c7-bfd970b9ae14)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Author](#author)

---

## Overview

CineAid combines a Chrome extension and a Python FastAPI to provide a user-friendly interface for accessing rich movie and TV series information. The Chrome extension dynamically fetches the title of the active tab, sends it to the FastAPI backend, which, in turn, utilizes web scraping to gather relevant data from various sources. The received information is then displayed in an organized and visually appealing popup.

---

## Features

- **Dynamic Information Retrieval:** CineAid fetches details about the current movie or TV series from the active browser tab, ensuring real-time and accurate data.

- **Comprehensive Data:** The project provides a wide array of information, including ratings from different platforms (IMDb, Rotten Tomatoes, MetaScore), genre, director, cast, reviews, and similar titles.

- **Seamless Integration:** The Chrome extension seamlessly integrates with your browsing experience, offering a non-intrusive popup for quick access to movie-related information.

- **Web Scraping Techniques:** The FastAPI backend employs web scraping techniques to extract relevant data from search engine results and dedicated movie-related pages.

---

## Installation

### Chrome Extension:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/cineaid.git
   ```

2. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the extension folder within the cloned repository.

### FastAPI Backend:

1. Install dependencies:

   ```bash
   pip install fastapi requests beautifulsoup4 lxml uvicorn
   ```

2. Run the FastAPI server:

   ```bash
   uvicorn cineaid_api_1:app --reload
   ```

3. Access the API in your browser:

   ```
   http://127.0.0.1:8000/movie_info/{browser_tab_title}
   ```

   Replace `{browser_tab_title}` with the title of the movie or TV series from the web browser tab.

---

## Usage

1. Activate the Chrome extension by clicking on the CineAid icon in your browser.

2. The popup automaticaly fetches information about the movie or TV series from the active tab and displays it in an organized table.

---



## Author

CineAid is created and maintained by Archit Roy. Feel free to reach out for any questions or feedback.

--- 

Thank you for using CineAid! Enjoy exploring the world of movies and TV series with ease and efficiency.




