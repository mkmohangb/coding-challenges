package main

import (
    "fmt"
    "net/http"
    "time"
)


func main() {
    links := []string {
        "http://google.com",
        "http://stackoverflow.com",
        "http://udemy.com",
    }

    ch := make(chan string)

    for _, l := range links {
        go checkLink(l, ch)
    }

    for l := range ch {
        go func(link string) {
            time.Sleep(3 * time.Second)
            checkLink(link, ch)
        }(l)
    }
}

func checkLink(link string, ch chan string) {
    _, err  := http.Get(link)
    if err != nil {
        fmt.Println(link, "link is not up")
        ch <- link
    }
    fmt.Println(link, "link is up")
    ch <- link
}


