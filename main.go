package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"strconv"
)

var WORDSET = map[string]bool{}

func main() {
	var dirPath string
	var rows = []*map[string]string{}
	fmt.Print("Enter path: ")
	fmt.Scanf("%s", &dirPath)

	files, err := ioutil.ReadDir(dirPath)
	if err != nil {
		log.Panic("error", err)
	}
	for _, file := range files {
		data, err := open(dirPath, file.Name())
		if err != nil {
			fmt.Println(err)
		}
		rows = append(rows, data)
	}
	csv := addToCsv(rows)
	err = os.WriteFile("summary.csv", []byte(csv), 777)
	if err != nil {
		log.Println("Error: ", err)
		return
	}
	log.Println("Successful !!!!")
}

func open(path, filename string) (*map[string]string, error) {
	filepath := fmt.Sprintf("%s/%s", path, filename)
	file, err := os.Open(filepath)
	if err != nil {
		log.Panic(err)
		return nil, err
	}
	return manageData(file, filename), nil
}

func manageData(file *os.File, filename string) *map[string]string {
	pattern := regexp.MustCompile(`.csv`)
	songTitle := pattern.ReplaceAllString(filename, "")
	data := make(map[string]string)
	reader := csv.NewReader(file)
	isHeader := true

	for {
		if isHeader {
			isHeader = false
			continue
		}

		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Printf("Error in file %s\n", file.Name())
		}
		data[record[0]] = record[1]
		data["title"] = songTitle
		if !WORDSET[record[0]] {
			WORDSET[record[0]] = true
		}
	}

	return &data
}

func parseInt(number string) int {
	num, err := strconv.Atoi(number)
	if err != nil {
		return 0
	}
	return num
}

func addToCsv(rows []*map[string]string) string {
	csv := ""
	count := 0
	wordList := []string{}

	for word := range WORDSET {
		if count < len(WORDSET)-1 {
			csv = fmt.Sprintf("%s,%s", csv, word)
			count++
		} else {
			csv = fmt.Sprintf("%s,%s\n", csv, word)
		}
		wordList = append(wordList, word)
	}

	for _, row := range rows {
		rowCsv := fmt.Sprintf("%s,", (*row)["title"])
		for _, word := range wordList {
			rowCsv = fmt.Sprintf("%s%d,", rowCsv, parseInt((*row)[word]))
		}
		csv = fmt.Sprintf("%s%s\n", csv, rowCsv)
	}

	return csv
}
