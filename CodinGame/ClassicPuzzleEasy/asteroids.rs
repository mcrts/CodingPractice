use std::io;
use std::collections::HashMap;

use itertools::Itertools;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

type Coordinate = (f32, f32);
type AsteroidMap = HashMap<char, Coordinate>;

fn parse_inputs() -> (i32, i32, i32, i32, i32, AsteroidMap, AsteroidMap) {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let inputs = input_line.split(" ").collect::<Vec<_>>();
    let w = parse_input!(inputs[0], i32);
    let h = parse_input!(inputs[1], i32);
    let t1 = parse_input!(inputs[2], i32);
    let t2 = parse_input!(inputs[3], i32);
    let t3 = parse_input!(inputs[4], i32);

    let mut as1= AsteroidMap::new();
    let mut as2= AsteroidMap::new();
    for j in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let row1 = inputs[0].trim().to_string();
        let row2 = inputs[1].trim().to_string();
        for i in 0..w as usize {
            let c1 = row1.chars().nth(i).unwrap();
            if c1 != '.' {
                as1.insert(c1, (j as f32, i as f32));
            } else {}
            let c2 = row2.chars().nth(i).unwrap();
            if c2 != '.' {
                as2.insert(c2, (j as f32, i as f32));
            } else {}
        }
    }
    return (w, h, t1, t2, t3, as1, as2);
}

fn diff(as1: &AsteroidMap, as2: &AsteroidMap) -> AsteroidMap {
    let mut asd = AsteroidMap::new();

    as1.iter().for_each(|(k, v)| {
        let (x1, y1) = v;
        let (x2, y2) = as2.get(k).unwrap();
        let d = (x2 - x1, y2 - y1);
        asd.insert(*k, d);
    });
    return asd
}

fn translate(as0: &AsteroidMap, asd: &AsteroidMap, dt: f32) -> AsteroidMap {
    let mut as1 = AsteroidMap::new();

    as0.iter().for_each(|(k, v)| {
        let (x, y) = v;
        let (dx, dy) = asd.get(k).unwrap();
        let f = (x + dt * dx, y + dt * dy);
        as1.insert(*k, f);
    });

    return as1
}

fn prepare_output(asm: &AsteroidMap, w: i32, h: i32) -> Vec<Vec<String>>{
    let mut grid = vec![vec![".".to_string(); w as usize]; h as usize];

    asm.iter()
        .sorted_by_key(|x| *x.0)
        .rev()
        .for_each(|(k, v)| {
        let x = v.0.floor() as i32;
        let y = v.1.floor() as i32;
        if (0 <= x) && (x < w) && (0 <= y) && (y < h) {
            grid[x as usize][y as usize] = k.to_string();
        } else {}
    });

    return grid
}


fn main() {
    
    let (w, h, t1, t2, t3, as1, as2) = parse_inputs();
    let dt = (t3 - t2) as f32/ (t2 - t1) as f32;
    let asd = diff(&as1, &as2);
    let as3 = translate(&as2, &asd, dt);
    let out = prepare_output(&as3, w, h);

    for i in 0..h as usize {
        let s = out[i].join("");
        println!("{}", s);

    }
}
