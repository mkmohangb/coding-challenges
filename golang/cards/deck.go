package main

import ("fmt"
        "math/rand"
        "os"
        "strings"
    )

type deck []string

func newDeck() deck {
    suites := []string{"Spades", "Hearts", "Diamonds", "Clubs"}
    values := []string{"Ace", "Two", "Three", "Four"}
    var cards deck

    for _, suit := range(suites) {
        for _, value := range(values) {
            cards = append(cards, value + " of " + suit)
        }
    }
    return cards
}

func deal(d deck, handSize int) (deck, deck) {
    return d[:handSize], d[handSize:]
}

func (d deck) print() {
    for i,card := range(d) {
        fmt.Println(i, card)
    }
}

func (d deck) toString() string {
    return strings.Join([]string(d), ",")
}

func (d deck) saveToFile(name string) error {
    return os.WriteFile(name, []byte(d.toString()), 0666)
}

func newDeckFromFile(name string) deck {
    bs, err := os.ReadFile(name)
    if (err != nil) {
        fmt.Println("Error: ", err)
        os.Exit(1)
    }
    s := strings.Split(string(bs), ",")
    return deck(s)
}

func (d deck) shuffle() {
    for i := range(d) {
        newPos := rand.Intn(len(d) - 1)
        d[i], d[newPos] = d[newPos], d[i]
    }
}
