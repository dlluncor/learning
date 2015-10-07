<?php

class Student {
  private $name;
  private $scores;

  public function __construct($name, $scores) {
    $this->name = $name;
    $this->scores = $scores;
  }

  public function getName() {
    return $this->name;
  }

  public function averageScore() {
    $sum = 0;
    foreach ($this->scores as $score) {
      $sum = $sum + $score;
    }
    return $sum / count($this->scores);
  }
}

function cmpStudents($a, $b) {
  $v0 = $a->averageScore();
  $v1 = $b->averageScore();
  if ($v0 == $v1) {
    return 0;
  }
  return ($v0 < $v1) ? 1 : -1;
}

$s0 = new Student('David L', [90, 86, 60, 10]);
$s1 = new Student('Jovani K', [92, 84, 83, 12]);
$s2 = new Student('Alexa O', [43, 23, 22, 5]);
$students = [$s0, $s1, $s2];
echo "Ranking of students:\n";
usort($students, "cmpStudents");
foreach ($students as $student) {
  $name = $student->getName();
  $avg = $student->averageScore();
  echo sprintf("%s \t(%.2f)\n", $name, $avg);
  //print "$name \t($avg)\n";
}


?>