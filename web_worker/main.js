var worker = {};

worker.main = function() {
  var blob = new Blob([document.querySelector('#woah').textContent]);
  var workerName = window.URL.createObjectURL(blob);
  var startTime = new Date();

  for (var i = 0; i < 7; i++) {
    var worker = new Worker(workerName);
    worker.addEventListener('message', function(e) {
      console.log('Worker ' + e.data.input.which + ' said: ', e.data.message);
    });
    var loc = document.location.href;

      worker.postMessage({url: loc, startTime: startTime, which: i});
    //setTimeout(postIt, 1);
  }
};
