package main

import (
  "fmt"
  "sort"
)

type Student struct {
  name string
  scores []int
}

func (s Student) score() float64 {
  val := 0.0
  for _, testScore := range s.scores {
    val += float64(testScore)
  }
  return val / float64(len(s.scores))
}

// ByAge implements sort.Interface for []Person based on
// the Age field.
type ByAge []Student

func (a ByAge) Len() int           { return len(a) }
func (a ByAge) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByAge) Less(i, j int) bool { return a[i].score() > a[j].score() }

func main() {
  fmt.Println("Ranking of students:");
  s1 := Student{
    "David L", []int{90, 86, 60, 10}};
  s2 := Student{
    "Jovani K", []int{92, 84, 83, 12}};
  s3 := Student{
    "Alexa O", []int{43, 23, 22, 5}};
  students := []Student{s1, s2, s3}
  sort.Sort(ByAge(students))
  for _, s := range students {
    fmt.Printf("%s \t(%.2f)\n", s.name,
      s.score())
  }
}