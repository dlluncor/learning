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
    return $sum; // count($this->scores);
  }
}

$s0 = new Student('David L', [90, 86, 60, 10]);
$s1 = new Student('Jovani K', [92, 84, 83, 12]);
$s2 = new Student('Alexa O', [43, 23, 22, 5]);
$students = [$s0, $s1, $s2];
echo "Ranking of students:\n";
foreach ($students as $student) {
  $name = $student->getName();
  $avg = $student->averageScore();
  print "$name \t ($avg)\n";
}


?>