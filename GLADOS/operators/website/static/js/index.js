function deleteSpotifyUsername(spotify_usernameId) {
    fetch("/delete-spotify_username", {
      method: "POST",
      body: JSON.stringify({ spotify_usernameId: spotify_usernameId }),
    }).then((_res) => {
      window.location.href = "/user-information";
    });
  }
function deleteSpotifyEmail(spotify_emailId) {
    fetch("/delete-spotify_email", {
      method: "POST",
      body: JSON.stringify({ spotify_emailId: spotify_emailId }),
    }).then((_res) => {
      window.location.href = "/user-information";
    });
  }
function deleteSpotifyPassword(spotify_passwordId) {
    fetch("/delete-spotify_password", {
      method: "POST",
      body: JSON.stringify({ spotify_passwordId: spotify_passwordId }),
    }).then((_res) => {
      window.location.href = "/user-information";
    });
  }
function deleteNetflixEmail(netflix_emailId) {
    fetch("/delete-netflix_email", {
      method: "POST",
      body: JSON.stringify({ netflix_emailId: netflix_emailId }),
    }).then((_res) => {
      window.location.href = "/user-information";
    });
  }
function deleteNetflixPassword(netflix_passwordId) {
    fetch("/delete-netflix_password", {
      method: "POST",
      body: JSON.stringify({ netflix_passwordId: netflix_passwordId }),
    }).then((_res) => {
      window.location.href = "/user-information";
    });
  }
  
  