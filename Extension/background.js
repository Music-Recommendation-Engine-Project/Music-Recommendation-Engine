/*
Part of this code was inspired by: https://javascript.plainenglish.io/use-spotify-to-login-to-your-chrome-extension-d60e21271c24
*/

const CLIENT_ID = encodeURIComponent('{SPOTIFY_CLIENT_ID}');
const RESPONSE_TYPE = encodeURIComponent('token');
const REDIRECT_URI = encodeURIComponent(
  `https://{extension_id}.chromiumapp.org/`
);
const SCOPE = encodeURIComponent(
  'user-read-email user-read-playback-state user-modify-playback-state'
);
const SHOW_DIALOG = encodeURIComponent('true');
let STATE = '';
let ACCESS_TOKEN = '';

let user_signed_in = false;

function create_spotify_endpoint() {
  STATE = encodeURIComponent(
    'meet' + Math.random().toString(36).substring(2, 15)
  );

  let oauth2_url = `https://accounts.spotify.com/authorize
?client_id=${CLIENT_ID}
&response_type=${RESPONSE_TYPE}
&redirect_uri=${REDIRECT_URI}
&state=${STATE}
&scope=${SCOPE}
&show_dialog=${SHOW_DIALOG}
`;

  console.log(oauth2_url);

  return oauth2_url;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'login') {
    if (user_signed_in) {
      console.log('User is already signed in.');
    } else {
      // sign the user in with Spotify
      chrome.identity.launchWebAuthFlow(
        {
          url: create_spotify_endpoint(),
          interactive: true,
        },
        function (redirect_url) {
          if (chrome.runtime.lastError) {
            sendResponse({ message: 'fail' });
          } else {
            if (redirect_url.includes('callback?error=access_denied')) {
              sendResponse({ message: 'fail' });
            } else {
              ACCESS_TOKEN = redirect_url.substring(
                redirect_url.indexOf('access_token=') + 13
              );
              ACCESS_TOKEN = ACCESS_TOKEN.substring(
                0,
                ACCESS_TOKEN.indexOf('&')
              );
              let state = redirect_url.substring(
                redirect_url.indexOf('state=') + 6
              );

              if (state === STATE) {
                console.log('SUCCESS');
                user_signed_in = true;

                setTimeout(() => {
                  ACCESS_TOKEN = '';
                  user_signed_in = false;
                }, 3600000);

                chrome.action.setPopup(
                  { popup: './popup-signed-in.html' },
                  () => {
                    sendResponse({ message: 'success' });
                  }
                );
              } else {
                sendResponse({ message: 'fail' });
              }
            }
          }
        }
      );
    }

    return true;
  } else if (request.message === 'logout') {
    user_signed_in = false;
    chrome.action.setPopup({ popup: './popup.html' }, () => {
      sendResponse({ message: 'success' });
    });
    return true;
  }
  if (request.message === 'get_access_token') {
    sendResponse({ accessToken: ACCESS_TOKEN });
  }
    if (request.message === 'fetch_recommended_artists') {
    fetch(
      `https://artist-api2023.herokuapp.com/find_similar_artists?artist=${encodeURIComponent(
        request.artistName
      )}&num_items=5`
    )
      .then((response) => response.json())
      .then((data) => sendResponse(data))
      .catch((error) => sendResponse({ error: error.message }));
    return true; // Required to use sendResponse asynchronously
  }
});

