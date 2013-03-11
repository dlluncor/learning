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

// Computes the sample standard deviation.
MyMath.sampleStdev = function(samples, n) {
  var mu = MyMath.mean(samples);
  var sumSq = 0;
  samples.forEach(function(sample) {
    sumSq += Math.pow(sample - mu, 2);
  });
  return sumSq / (n - 1);
};

// Is the mean within the range of these two values?
MyMath.isMeanWithinRange = function(lower, upper, meanVal) {
  if (meanVal < lower) {
    return false;
  } else if (meanVal > upper) {
    return false;
  }
  return true;
};

var Stats = {};

Stats = function(distrib) {
  this.distrib = distrib;
};

// Take a sample n times and return the mean.
Stats.prototype.sampleMeanInfo = function(n) {
  if (n == 0) {
    throw Error('This is a problem.');
  }
  var N = this.distrib.length;

  var sum = 0;
  var samples = []; // samples taken during estimate.
  for (var i = 0; i < n; i++) {
    var index = Math.floor(Math.random() * N);
    if (index == N) {
      index = N - 1;
    }
    sum += this.distrib[index];
    samples.push(this.distrib[index]);
  }
  var sampleMeanInfo = {
    'sampleMean': sum / n,
    'n': n,
    'samples': samples
  };
  return sampleMeanInfo;
};

// Generate a sample distribution for a given number of trials
// and a certain number of samples.
Stats.prototype.sampleDistributionInfo = function(trials, n) {
  var meanInfos = [];

  for (var i = 0; i < trials; i++) {
    meanInfos.push(this.sampleMeanInfo(n));
  }
  return meanInfos;
}

Stats.getDistributions = function(sampleMeanInfos) {
  return sampleMeanInfos.map(function(sampleMeanInfo) {
    return sampleMeanInfo.sampleMean;
  });
};

// First level characteristics of a list of numbers.
Stats.firstLevelStats = function(distrib) {
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

// Second level characteristics like likelihood the actual
// mean falls within the bounds estimated by each of the numbers
// in the distribution.
Stats.secondLevelStats = function(sampleMeanInfos, actualMean) {
  // Need samples taken, n, and mean of samples.

  // Number of times we estimated the mean was within our range
  // correctly.
  var numTimesInRange = 0;

  sampleMeanInfos.forEach(function(sampleMeanInfo) {
    var n = sampleMeanInfo.n;
    var s = MyMath.sampleStdev(sampleMeanInfo.samples, n);
    var stdevOfSamplingDistrib = s / Math.sqrt(n);
    var mu_sampleMean = sampleMeanInfo.sampleMean;

    // Compute 95% confidence your estimate falls in this range.
    var oneSideRange = 1.96 * stdevOfSamplingDistrib;
    var lowerRange = mu_sampleMean - oneSideRange;
    var upperRange = mu_sampleMean + oneSideRange;
    var text = mu_sampleMean + ' [ ' + lowerRange + ',' + upperRange + ']';
    var isMeanInRange = MyMath.isMeanWithinRange(lowerRange, upperRange, actualMean);
    if (isMeanInRange) {
      text += ' YES';
      numTimesInRange += 1;
    } else {
      text += ' NO';
    }
    //print (text);
  });

  print ('Prob predicted correct: ' + (numTimesInRange / sampleMeanInfos.length) * 100);
}

var Shower = function() {
};

// Prints a distribution of numbers.
Shower.prototype.show = function(distrib) {
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

ctrl.getOriginalDistribution = function() {
  var distribCsv = $('#distrib').val();
  var els = distribCsv.split(',');
  var distrib = [];
  els.forEach(function(el) {
    distrib.push(parseInt(el));
  });
  return distrib;
};

ctrl.init = function() {
 var distrib = [1, 1, 1, 1, 1, 1, 1, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 10, 10, 10, 10, 10]; 
 var distribStr = distrib.join(',');
 $('#distrib').val(distribStr);
 ctrl.runStats();
};

ctrl.runStats = function() {
  ctrl.clearEls();
  var myInput = ctrl.getInput();

  print('Population parameters:');
  var origDistrib = ctrl.getOriginalDistribution();
  Stats.firstLevelStats(origDistrib);
  var origMean = MyMath.mean(origDistrib);

  var show0 = new Shower();
  show0.show(origDistrib);

  print('Sampling parameters:');

  var woah = new Stats(origDistrib);
  var distribInfo = woah.sampleDistributionInfo(myInput.trials, myInput.n);
  var distrib = Stats.getDistributions(distribInfo);
  show0.show(distrib);
  // Get first level characteristics.
  Stats.firstLevelStats(distrib);
  // Get z stat inferential characteristics.
  Stats.secondLevelStats(distribInfo, origMean);
};

$(document).ready(ctrl.init);
