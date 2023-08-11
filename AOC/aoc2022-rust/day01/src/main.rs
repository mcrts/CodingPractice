use std::io;
use std::io::BufRead;

pub type Error = Box<dyn std::error::Error + Send + Sync>;
pub type Result<T> = std::result::Result<T, Error>;

type Elf = Vec<i32>;


fn parse_input<B: BufRead>(lines: io::Lines<B>) -> Vec<Elf> {
    let mut elves = Vec::<Elf>::new();
    let mut elve = Elf::new();

    for line in lines {
        match line {
            Err(error) => panic!("Problem reading stdin: {:?}", error),
            Ok(s) => match s.as_str() {
                "" => {
                    elves.push(elve.clone());
                    elve.truncate(0);
                },
                s => elve.push(s.parse::<i32>().unwrap()),
            },
        };
    }
    elves.push(elve.clone());
    return elves
}

fn find_maximum(elves: &Vec<Elf>) -> i32 {
    let mut results = Vec::<i32>::new();

    for elf in elves {
        results.push(elf.iter().sum());
    }

    let m = results.iter().max().unwrap();
    return *m;
}

fn find_top3(elves: &Vec<Elf>) -> i32 {
    let mut v1: i32 = 0;
    let mut v2: i32 = 0;
    let mut v3: i32 = 0;
    for elf in elves {
        let v = elf.iter().sum();
        if v > v1 {
            v3 = v2;
            v2 = v1;
            v1 = v;
        } else if v > v2 {
            v3 = v2;
            v2 = v;
        } else if v > v3 {
            v3 = v;
        }
    }
    return v1 + v2 + v3;
}

pub fn main() {
    let lines = io::stdin().lock().lines();
    let elves = parse_input(lines);
    let calories = find_maximum(&elves);
    let top3_calories = find_top3(&elves);
    println!("{:?}", calories);
    println!("{:?}", top3_calories);
}