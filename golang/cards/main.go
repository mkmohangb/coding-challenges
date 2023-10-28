package main

import "fmt"


func main() {
    // cards := newDeck()
    // hand, remaining := deal(cards, 5)
    // hand.print()
    // fmt.Println("---------")
    // remaining.print()
    //cards.saveToFile("my_cards")
    cards := newDeckFromFile("my_cards")
    cards.shuffle()
    fmt.Println(cards.toString())
}
