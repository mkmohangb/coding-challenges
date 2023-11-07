package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/mediocregopher/radix/v4"
)

func main() {
	ctx := context.TODO()
	client, err := (radix.PoolConfig{}).New(ctx, "tcp", "127.0.0.1:6379")
	if err != nil {
		// handle error
		fmt.Println("Error when connecting to redis server: ", err)
		os.Exit(1)
	}
	err = client.Do(ctx, radix.Cmd(nil, "SET", "foo", "bar"))

	var fooVal string
	err = client.Do(ctx, radix.Cmd(&fooVal, "GET", "foo"))
	fmt.Println("retrieved value of foo is ", fooVal)

	p := radix.NewPipeline()
	p.Append(radix.FlatCmd(nil, "SET", "foo", 1))
	p.Append(radix.Cmd(&fooVal, "GET", "foo"))

	if err := client.Do(ctx, p); err != nil {
		panic(err)
	}

	log.Printf("fooVal: %s\n", fooVal)

}
