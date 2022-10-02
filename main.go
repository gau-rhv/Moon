

// GO language program with an example of Hash Table

package main

import (
"fmt"
)

func main() {
	var country map[int]string
	country = make(map[int] string)
	country[1]="India"
	country[2]="China"
	country[3]="Pakistan"
	country[4]="Germany"
	country[5]="Australia"
	country[6]="Indonesia"
	for i, j := range country {
		fmt.Printf("Key: %d Value: %s\n", i, j)
	}
}


