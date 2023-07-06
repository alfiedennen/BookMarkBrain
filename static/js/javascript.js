document.addEventListener('DOMContentLoaded', () => {

    // Handler for form submission
    document.getElementById("searchForm").addEventListener('submit', function(e) {
      e.preventDefault();
      const keyword = document.getElementById("search").value;
      if (keyword !== '') {
          window.location.href = "/search?keyword=" + keyword;
      }
    });
  
    function loadResults() {
        console.log("Executing loadResults function...");
        const urlParams = new URLSearchParams(window.location.search);
        const keyword = urlParams.get('keyword');
        fetch(`/api/search?keyword=${keyword}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Fetched /api/search results: ", data);
                displaySearchResults(data)
            })
            .catch(error => {
                console.error('There was an error fetching the search results!', error);
            });
    }
  
    // Get the initial wordFrequency data when the page loads
    fetch("/api/wordFrequency")
    .then(response => response.json())
    .then(data => {
        console.log("Fetched api/wordFrequency: ", data);
        displayWordCloud(data);
    })
  
    // Call loadResults function if on the search page
    if (window.location.pathname === '/search') {
        loadResults();
    }
  });
  
  function displayWordCloud(wordFrequency) {
      console.log("Calling displayWordCloud with: ", wordFrequency);
  
      let wordCloudInput = [];
      for (let word in wordFrequency) {
          wordCloudInput.push([word, wordFrequency[word]]);
      }
  
      // Sort by frequency
      wordCloudInput.sort(function(a, b) { return b[1] - a[1]; });
  
      // Limit to top 300 words
      wordCloudInput = wordCloudInput.slice(0, 300);
      
      console.log(wordCloudInput);
      
      // Call WordCloud on the container with input data
      WordCloud(document.getElementById('word-cloud-container'), {
          list: wordCloudInput,
          click: function(item) {
              // Upon click, just redirect to the search page with the clicked word as the keyword
              window.location.href = "/search?keyword=" + encodeURIComponent(item[0]);
          }
      });
  }

  WordCloud(document.getElementById('word-cloud-container'), {
    list: wordCloudInput,
    click: function(item) {
        // Upon click, just redirect to the search page with the clicked word as the keyword
        window.location.href = "/search?keyword=" + encodeURIComponent(item[0]);
    }
});

const wordCloudContainer = document.getElementById('word-cloud-container');
WordCloud(wordCloudContainer, {
    list: wordCloudInput,
    gridSize: Math.round(wordCloudContainer.clientWidth / 32),
    click: function(item) {
        // Upon click, just redirect to the search page with the clicked word as the keyword
        window.location.href = "/search?keyword=" + encodeURIComponent(item[0]);
    }
});
  
function displaySearchResults(data) {
    console.log("Calling displaySearchResults with: ", data);
    const container = document.getElementById('search-results');
    container.innerHTML = '';
    data.forEach(row => {
        // Use row.url directly for the href attribute
        const div = document.createElement('div');
        div.innerHTML = `
        <h2><a href="${row.url}" target="_blank" rel="noopener noreferrer">${row.url}</a></h2>
        <p>Content: ${row.content}</p>
        <p>Topics: ${row.topics}</p>
        <p>Keywords: ${row.keywords}</p>
        `;
        container.appendChild(div);
    });
}