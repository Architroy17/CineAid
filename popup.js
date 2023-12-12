//created by archit roy
//this code, takes chrome browser tab title, sends it to api, receives data from it and then displays it.



let tabtitle; // Variable to store the title of the current tab
const getTabtitle = new Promise(resolve => { // Promise to get the title of the currently active tab
    chrome.tabs.query({ // Query the Chrome tabs API to get information about the active tab in the current window
        active: true, //if tab active and current window
        currentWindow: true
    }, function(tabs) {
        tabtitle = tabs[0].title; // Extract the title of the first tab in the array (assuming it exists)
        resolve(tabtitle);// Resolve the promise with the extracted title
    });
});

getTabtitle.then(title => { //title is resolved value of promise which is tabtitle
    document.getElementById("title").textContent = title; // Use the promise to set the title in the HTML element with the id "title"
});



// Function to make a request to the hosted API 
//this function sends title and receives,gets    information and stores it in data 
const fetchDataFromAPI = async (title) => { //async to better coordinate with promises
    try {
    // Construct the API endpoint
        const apiEndpoint = `https://cineaid.onrender.com/movie_info/${encodeURIComponent(title)}`;
     // Make a GET request to the API
        const response = await fetch(apiEndpoint);
        //check if request succesful?
        if (!response.ok) {
            throw new Error("API request failed");
        }
        // Parse the JSON response
        const data = await response.json();
        //return parsed data
        return data;
    }    
    catch (error) {
        console.error("Error fetching data from API:", error);// Handle errors, log the error to the console
    return null;// Return null in case of an error
    }
};

// Function to update the popup HTML with the received data
const updatePopupHTML = (data) => {
  // Update the HTML elements with the received data
    document.getElementById("title").textContent = data.title;
    document.getElementById("genre").textContent = data.geanre;
    document.getElementById("director").textContent = data.director;
    document.getElementById("cast").textContent = data.cast.join(", ");
    document.getElementById("imdb_ratings").textContent = data.ratings[0];
    document.getElementById("rotten_ratings").textContent = data.ratings[1];
    document.getElementById("meta_ratings").textContent = data.ratings[2];
    document.getElementById("similar").textContent = data.similar.join(", ");
    document.getElementById("reviews").textContent = data.review.join(", ");
};

// Use the promise to get the tab title and fetch data from the API
getTabtitle.then(async (tabtitle) => {
  // Make a request to the hosted API
    const data = await fetchDataFromAPI(tabtitle);
  // Update the popup HTML with the received data
    if (data) {
        updatePopupHTML(data);
    } 
    else {
    // Handle the case where data couldn't be fetched
        console.error("Failed to fetch data from the API");
    }
});
