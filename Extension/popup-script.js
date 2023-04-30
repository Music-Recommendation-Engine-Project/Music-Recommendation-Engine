document.querySelector('#sign-in').addEventListener('click', function () {
  chrome.runtime.sendMessage({ message: 'login' }, function (response) {
    if (response.message === 'success') window.close();
  });
});
