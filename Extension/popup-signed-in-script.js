// popup-signed-in-script.js
document.getElementById('sign-out').addEventListener('click', () => {
  chrome.runtime.sendMessage({ message: 'logout' }, (response) => {
    if (response.message === 'success') window.close();
  });
});

function cleanName(name) {
  let cleanedName = name;

  const dashIndex = name.indexOf('-');
  if (dashIndex !== -1) {
    cleanedName = name.substring(0, dashIndex).trim();
  }

  const parenIndex = name.indexOf('(');
  if (parenIndex !== -1) {
    cleanedName = cleanedName.substring(0, parenIndex).trim();
  }

  return cleanedName;
}

async function getAccessTokenFromBackgroundPage() {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ message: 'get_access_token' }, (response) => {
      resolve(response.accessToken);
    });
  });
}

async function getCurrentSong(accessToken) {
  const response = await fetch(
    'https://api.spotify.com/v1/me/player/currently-playing',
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (response.status === 200) {
    const data = await response.json();
    const songInfo = `${data.item.name}`;
    const cleanedSongInfo = cleanName(songInfo); // Clean the song name
    const artistInfo = `${data.item.artists
      .map((artist) => artist.name)
      .join(', ')}`;
    document.getElementById('current-song').innerText = cleanedSongInfo; // Display the cleaned song name
    document.getElementById('current-artist').innerText = artistInfo;

    // Fetch recommended artists
    const firstArtist = data.item.artists[0].name;
    fetchRecommendedArtists(accessToken, firstArtist);

    // Update the album image
    const albumCoverUrl = data.item.album.images[0].url;
    document.getElementById('album-cover').src = albumCoverUrl;

    // Set the background color based on the dominant color in the album cover
    const colorThief = new ColorThief();
    document.getElementById('album-cover').addEventListener('load', () => {
      const color = colorThief.getColor(document.getElementById('album-cover'));
      document.body.style.backgroundColor = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
    });
  } else {
    document.getElementById('current-song').innerText =
      'No song is currently playing.';
  }
}

async function previousSong(accessToken) {
  await fetch('https://api.spotify.com/v1/me/player/previous', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  // Refresh the current song information after changing the song
  getCurrentSong(accessToken);
}

async function nextSong(accessToken) {
  await fetch('https://api.spotify.com/v1/me/player/next', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  // Refresh the current song information after changing the song
  getCurrentSong(accessToken);
}

// Function to refresh the current song information periodically
async function startPeriodicSongUpdates(accessToken) {
  // Refresh the song information every 5 seconds (5000 milliseconds)
  const refreshInterval = 2000;

  setInterval(async () => {
    getCurrentSong(accessToken);
  }, refreshInterval);
}

(async function () {
  const accessToken = await getAccessTokenFromBackgroundPage();

  // Add event listeners for the "Next" and "Previous" buttons
  // Add event listeners for the "Previous" and "Previous" buttons
  document.getElementById('previous').addEventListener('click', () => {
    previousSong(accessToken);
  });

  document.getElementById('next').addEventListener('click', () => {
    nextSong(accessToken);
  });

  getCurrentSong(accessToken);
  startPeriodicSongUpdates(accessToken);
})();

const recommender = document.createElement('p');
recommender.id = 'recommender-engine';
const leftside = document.getElementById('left-side');
leftside.appendChild(recommender);


function displayRecommendedArtists(recommendedArtists) {
  const recommendedTitle = document.getElementById('Recommended_title');
  let ul = document.getElementById('recommended-artists-list');

  if (!ul) {
    ul = document.createElement('ul');
    ul.id = 'recommended-artists-list';
    recommendedTitle.parentNode.insertBefore(ul, recommendedTitle.nextSibling);
  }

  ul.innerHTML = '';

  recommendedArtists.forEach((artist) => {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.id = 'play-button';
    link.href = '#';
    link.innerText = ` | Play`;
    link.addEventListener('click', async () => {
      try {
        const accessToken = await getAccessTokenFromBackgroundPage();
        const artistSearchResponse = await fetch(
          `https://api.spotify.com/v1/search?q=${encodeURIComponent(
            artist
          )}&type=artist&limit=1`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        if (artistSearchResponse.status === 200) {
          const searchData = await artistSearchResponse.json();
          const artistId = searchData.artists.items[0].id;

          await fetch('https://api.spotify.com/v1/me/player/play', {
            method: 'PUT',
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              context_uri: `spotify:artist:${artistId}`,
            }),
          });
        } else {
          console.error('Error searching for artist:', artist);
        }
      } catch (error) {
        console.error('Error playing artist:', artist, error);
      }
    });
    li.innerText = artist;
    li.appendChild(link);
    ul.appendChild(li);
  });
}


let currentArtist = '';

async function fetchRecommendedArtists(accessToken, artistName) {
  if (artistName !== currentArtist) {
    currentArtist = artistName;

    try {
      const customApiResponse = await fetchCustomAPI(artistName, accessToken);
      if (customApiResponse.success) {
        const recommendedArtists = customApiResponse.data.slice(1); // Remove the first artist from the list
        displayRecommendedArtists(recommendedArtists);
        recommender.innerText = '*Using BPR Algorithm';
      } else {
        throw new Error('Custom API response not successful');
      }
    } catch (error) {
      console.error('Error fetching from custom API:', error);
      const spotifyApiResponse = await fetchSpotifyAPI(artistName, accessToken);
      const recommendedArtists = spotifyApiResponse.tracks.map(
        (track) => track.artists[0].name
      );
      displayRecommendedArtists(recommendedArtists);
      recommender.innerText = '*Using Spotify Engine';
    }
  }
}


async function fetchCustomAPI(artistName, accessToken) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(
      {
        message: 'fetch_recommended_artists',
        artistName: artistName,
        accessToken: accessToken,
      },
      (data) => {
        if (data.error) {
          reject(data.error);
        } else {
          resolve({ success: true, data: data });
        }
      }
    );
  });
}

async function fetchSpotifyAPI(artistName, accessToken) {
  const artistSearchResponse = await fetch(
    `https://api.spotify.com/v1/search?q=${encodeURIComponent(
      artistName
    )}&type=artist&limit=1`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (artistSearchResponse.status === 200) {
    const searchData = await artistSearchResponse.json();
    const artistId = searchData.artists.items[0].id;

    const recommendationsResponse = await fetch(
      `https://api.spotify.com/v1/recommendations?seed_artists=${artistId}&limit=4`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (recommendationsResponse.status === 200) {
      const recommendationsData = await recommendationsResponse.json();
      return recommendationsData;
    } else {
      throw new Error('Error fetching artist from Spotify API');
    }
    
  }
  else {
    throw new Error('Error fetching artist from Spotify API');
  }
    
}


async function playSong(accessToken, artistName) {
  const artistSearchResponse = await fetch(
    `https://api.spotify.com/v1/search?q=${encodeURIComponent(
      artistName
    )}&type=artist&limit=1`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (artistSearchResponse.status === 200) {
    const searchData = await artistSearchResponse.json();
    const artistId = searchData.artists.items[0].id;

    const topTracksResponse = await fetch(
      `https://api.spotify.com/v1/artists/${artistId}/top-tracks?country=US`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (topTracksResponse.status === 200) {
      const topTracksData = await topTracksResponse.json();
      const topTrack = topTracksData.tracks[0];
      const trackId = topTrack.id;
      const trackUri = topTrack.uri;

      await fetch(
        `https://api.spotify.com/v1/me/player/play?device_id=${deviceId}`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({
            uris: [trackUri],
          }),
        }
      );
    } else {
      throw new Error('Error fetching top tracks from Spotify API');
    }
  } else {
    throw new Error('Error fetching artist from Spotify API');
  }
}

async function getTopSongByArtist(accessToken, artistName) {
  const artistSearchResponse = await fetch(
    `https://api.spotify.com/v1/search?q=${encodeURIComponent(
      artistName
    )}&type=artist&limit=1`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (artistSearchResponse.status === 200) {
    const searchData = await artistSearchResponse.json();
    const artistId = searchData.artists.items[0].id;

    const topTracksResponse = await fetch(
      `https://api.spotify.com/v1/artists/${artistId}/top-tracks?market=US`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (topTracksResponse.status === 200) {
      const topTracksData = await topTracksResponse.json();
      return topTracksData.tracks[0].id;
    } else {
      throw new Error('Error fetching top tracks from Spotify API');
    }
  } else {
    throw new Error('Error fetching artist from Spotify API');
  }
}
