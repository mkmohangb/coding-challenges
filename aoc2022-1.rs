// From: https://fasterthanli.me/series/advent-of-code-2022/part-1
use color_eyre;
use itertools::Itertools;
use std::io;

fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;
    println!("Select one of the approaches: \n 1. Imperative \n 2. Using iterators \n 3. Using itertools batching\
     \n 4. Using itertools coalesce");
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Failed to read line");
    let choice:usize = input.trim().parse().unwrap();

    match choice {
        1 => {
        // approach 1 - imperative 
        //let input = std::fs::read_to_string("src/input.txt").expect("while reading src/input.txt");
        let mut max = 0;
        let input = include_str!("input.txt");
        for group in input.split("\n\n") {
            println!("In Group");
            let mut sum = 0;
            for line in group.lines() {
                let value = line.parse::<u64>()?;
                println!(" - {value}");
                sum += value;
            }
            if sum > max {
                max = sum;
            }
        }
        println!("the max calories is {max}");
    },
    2 => {

        // approach 2 - using iter & closures
        let lines = include_str!("input.txt")
                    .lines()
                    .map(|line| line.parse::<u64>().ok())
                    .collect::<Vec<_>>();
        let lead = lines.split(|line| line.is_none())
                        .map(|group| group.iter().map(|v| v.unwrap()).sum::<u64>())
                        .max();
        println!("the max calories is {lead:?}");
    },

    3 => {   
        // approach 3 - using itertools batching
        let max = include_str!("input.txt")
                        .lines()
                        .map(|line| line.parse::<u64>().ok())
                        .batching(|it| {
                                let mut sum = None;
                                while let Some(Some(v)) = it.next() {
                                    sum = Some(sum.unwrap_or(0) + v);
                                }
                                sum
                            })
                        .max();
        println!("the max calories is {max:?}");
    },
                    
    4 => {
        // approach 4 - using itertools coalesce
        let max = include_str!("input.txt")
                    .lines()
                    .map(|line| line.parse::<u64>().ok())
                    .coalesce(|a, b| match(a, b) {
                            (None, None) => Ok(None),
                            (None, Some(a)) => Ok(Some(a)),
                            (Some(a), Some(b)) => Ok(Some(a+b)),
                            (Some(a), None) => Err((Some(a), None))
                            })
                    .max()
                    .flatten()
                    .unwrap();
                            
        println!("the max calories is {max:?}");
    },
    _ => println!("Invalid option")
  }

Ok(())
}
