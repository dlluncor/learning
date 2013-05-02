package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"container/list"
)

func getMaxDivers(G int, B int) int {
	var big = G
	var little = B
	if B > G {
		big = B
		little = G
	}
	if big == 0 && little == 0 {
		return 0
	}
	var left = big - 1 - little
	if left <= 0 {
		return 1
	}
	var beforeCeil = float64(left) / float64(little+1.0)
	var extra = int(math.Ceil(beforeCeil))
	return extra + 1
}

func GirlsBoys() {
	in := bufio.NewReader(os.Stdin)
	for {
		line, _ := in.ReadString('\n')
		line = strings.Replace(line, "\n", "", -1)
		if line == "0 0" {
			break
		}
		elements := strings.Split(line, " ")
		G, _ := strconv.Atoi(elements[0])
		B, _ := strconv.Atoi(elements[1])
		val := getMaxDivers(G, B)
		fmt.Printf("%d", val)
	}
}

type Point struct {
  Row int
  Col int
}

type Info struct {
  Seen bool
  Dist int
}

type Bitmapper struct {
  valueMap map[Point] *Info
  q *list.List
  numRows int
  numCols int
}

func (b *Bitmapper) ReadInput(in *bufio.Reader) {
  b.q = list.New()
  b.valueMap = make(map[Point] *Info)
  line := rawInput(in)
  elements := strings.Split(line, " ")
  numRows, _ := strconv.Atoi(elements[0])
  numCols, _ := strconv.Atoi(elements[1])
  b.numRows = numRows
  b.numCols = numCols
  for i := 0; i < numRows; i++ {
    colLine := rawInput(in)
    colArr := strings.Split(colLine, "")
    for j := 0; j < numCols; j++ {
      val, _ := strconv.Atoi(colArr[j])
      point := Point{i, j}
      if val == 1 {
        b.valueMap[point] = &Info{true, 0}
	b.q.PushBack(point)
        //fmt.Printf("pushing a 1") 
      } else {
        b.valueMap[point] = &Info{false, -1}
      }
    }
  }
}

func (b *Bitmapper) Solve() {
  for ; b.q.Len() > 0; {
    // Pop from the front of the queue.
    el := b.q.Front()
    p := el.Value.(Point)
    b.q.Remove(el)
    curInfo := b.valueMap[p]
    newDistance := curInfo.Dist + 1
    
    // Create neighbors to look through.
    up := Point{p.Row-1, p.Col}
    down := Point{p.Row+1, p.Col}
    left := Point{p.Row, p.Col-1}
    right := Point{p.Row, p.Col+1}
    neighs := [4]Point{up, down, left, right}
    for _, neigh := range neighs {
      // Remove neighbors which are not in the map.
      if _, ok := b.valueMap[neigh]; !ok {
        continue
      }
      pointInfo, _ := b.valueMap[neigh]

      if pointInfo.Dist == -1 {
        pointInfo.Dist = newDistance 
      } else { 
        // For each neighbor, did I find a shorter path?
        if newDistance < pointInfo.Dist {
          pointInfo.Dist = newDistance
          pointInfo.Seen = false // Need to investigate this point again and put on queue
        }
      }

      // Add the neighbor to explore if we haven't looked at it yet.
      if !pointInfo.Seen {
        b.q.PushBack(neigh)
      }
    }
    curInfo.Seen = true // Ive explored this node now
  }

  // Print out the distances in a string.
  lines := make([]string, b.numRows)
  for i := 0; i < b.numRows; i++ {
    lineStrs := make([]string, b.numCols)
    for j := 0; j < b.numCols; j++ {
      p := Point{i, j}
      pointInfo, _ := b.valueMap[p]
      lineStrs[j] = strconv.Itoa(pointInfo.Dist)
    }
    lines[i] = strings.Join(lineStrs, " ")
  }
  answer := strings.Join(lines, "\n")
  fmt.Printf("%s", answer)
}

 

func rawInput(reader *bufio.Reader) string {
  line, _ := reader.ReadString('\n')
  line = strings.Replace(line, "\n", "", -1)
  return line
}

func Bitmap() {
  in := bufio.NewReader(os.Stdin)
  line := rawInput(in)
  T, _ := strconv.Atoi(line)
  for i := 0; i < T; i++ {
    bm := &Bitmapper{}
    bm.ReadInput(in)
    bm.Solve()
  }
}

func main() {
	//GirlsBoys()
  Bitmap()
}
