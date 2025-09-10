use std::env;
use std::fs::File;
use std::path::Path;
use std::io::{self, BufRead};
use std::collections::HashSet;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn part01(filepath: &String) -> i32 {
    let mut conjugate_set = HashSet::new();

    if let Ok(lines) = read_lines(filepath) {
        for line in lines.map_while(Result::ok) {
            let d = line.parse::<i32>().unwrap();
            if conjugate_set.contains(&d) {
                return d * (2020 - d);
            } else {
                conjugate_set.insert(2020 - d);
            }
        }
    } else {
        panic!("Unable to read file {filepath}.");
    }

    panic!("Couldn't find a solution !");
}

fn part02(filepath: &String) -> i32 {
    let mut account = HashSet::new();

    if let Ok(lines) = read_lines(filepath) {
        for line in lines.map_while(Result::ok) {
            let d = line.parse::<i32>().unwrap();
            account.insert(d);
        }
    } else {
        panic!("Unable to read file {filepath}.");
    }

    for a in &account {
        for b in &account {
            if account.contains(&(2020 - a - b)) {
                return a * b * (2020 - a - b);
            }
        }
    }
    
    panic!("Couldn't find a solution !");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filepath = &args[1];

    let part01 = part01(filepath);
    println!("Day01 Part01 | {part01}");

    let part02 = part02(filepath);
    println!("Day01 Part02 | {part02}");
}