var $ = {};

$.set = function(id, html) {
  var el = document.getElementById(id);
  el.innerHTML = html;
}

var Student = function(name, grades) {
  this.name = name;
  this.grades = grades;
}

Student.prototype.average_score = function() {
  var sum = 0;
  for (var i = 0; i < this.grades.length; i++) {
    sum += this.grades[i];
  }
  return sum / this.grades.length;
}

var ctrl = {};

ctrl.main = function() {
  var s1 = new Student("David L", [90, 86, 60, 10]);
  var s2 = new Student('Jovani K', [92, 84, 83, 12]);
  var s3 = new Student('Alexa O', [43, 23, 22, 5]);
  var students = [s1, s2, s3];
  var str = "";
  students.sort(function(a, b) {return a.average_score() < b.average_score();});
  for (var i = 0; i < students.length; i++) {
    var s = students[i];
    str += "<div>"
    str += s.name + " \t(" + s.average_score() + ")";
    str += "</div>";
  }
  $.set('force', str);
}

ctrl.main();