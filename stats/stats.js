var print = function(str) {
  window.console.log(str);
  $('#canvas').append('<div>' + str + '</div>'); 
};

var MyMath = {};

// Gets the mean of an array.
MyMath.mean = function(arr) {
  var sum = 0;
  arr.forEach(function(el) {
    sum += el;
  });
  return sum / arr.length;
};

var stats = {};

stats = function(distrib) {
  this.distrib = distrib;
};

// Take a sample n times and return the mean.
stats.prototype.sampleMean = function(n) {
  if (n == 0) {
    throw Error('This is a problem.');
  }
  var N = this.distrib.length;

  var sum = 0;
  for (var i = 0; i < n; i++) {
    var index = Math.floor(Math.random() * N);
    if (index == N) {
      index = N - 1;
    }
    sum += this.distrib[index];
  }
  return sum / n;
};

// Generate a sample distribution for a given number of trials
// and a certain number of samples.
stats.prototype.sampleDistribution = function(trials, n) {
  var means = [];

  for (var i = 0; i < trials; i++) {
    means.push(this.sampleMean(n));
  }
  return means;
}

// First level characteristics of a list of numbers.
stats.prototype.firstLevelStats = function(distrib) {
  var n = distrib.length;
  // Mean.
  var mean = MyMath.mean(distrib);
  print ('Mean: ' + mean);

  // Skew.
  var sumSq = 0;  // sum squared from mean.
  var sumCu = 0;  // sum cubed from mean.
  distrib.forEach(function(el) {
    sumSq += Math.pow((el - mean), 2);
    sumCu += Math.pow((el - mean), 3);
  });
  var numer = sumCu / n;
  var denom = Math.pow(Math.pow(sumSq / n, 3), 0.5);
  var skew = numer / denom;

  print('Skew: ' + skew);

  // Kurtosis.
  sumSq = 0;
  var sumQu = 0;
  distrib.forEach(function(el) {
    sumSq += Math.pow((el - mean), 2);
    sumQu += Math.pow((el - mean), 4);
  });
  var kuNumer = sumQu / n;
  var kuDenom = Math.pow((sumSq / n), 2);
  var kurtosis = (kuNumer / kuDenom) - 3;
  print ('Kurtosis: ' + kurtosis);

};

var shower = function() {
};

// Prints a distribution of numbers.
shower.prototype.show = function(distrib) {
  // Get list of numbers with their probability of occuring.
  var probs = {};
  // Compute an object with the number and its probability of occuring.
  distrib.forEach(function(el) {
    if (!(el in probs)) {
      probs[el] = 0;
    }

    probs[el] += 1;
  });

  var mydata = [];

  for (sampleNumber in probs) {
    var freq = probs[sampleNumber] / distrib.length;
    mydata.push({
      'letter': sampleNumber,
      'frequency' : freq
    });
  }

  var sortF = function(a, b) {
    var diff = a.letter - b.letter;
    var num = diff / Math.abs(diff);
    return num;
  };

  mydata.sort(sortF);

  print(mydata[Math.floor(mydata.length / 2)].letter);

  // var mydata = [];
  // mydata.push({'letter': 'A', 'frequency': 0.2});
  barchart.renderBars(mydata, 'canvas');
};

var ctrl = {};

ctrl.clearEls = function() {
  $('#canvas').html('');
};

// returns an object {trials: number, n: number}
ctrl.getInput = function() {
  var trials = parseInt($('#trials').val());
  var n = parseInt($('#samples').val());
  return {
    'trials': trials,
    'n': n
  };
}

ctrl.init = function() {
  ctrl.clearEls();
  var myInput = ctrl.getInput();

  var origDistrib = [1, 1, 1, 1, 1, 1, 1, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 10, 10, 10, 10, 10]; 
  //var origDistrib = [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 12, 1, 10]; 
  var show0 = new shower();
  show0.show(origDistrib);

  var woah = new stats(origDistrib);
  var distrib = woah.sampleDistribution(myInput.trials, myInput.n);
  show0.show(distrib);
  // Get first level characteristics.
  woah.firstLevelStats(distrib);
};

$(document).ready(ctrl.init);
