use std::io;
use std::vec::Vec;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

#[derive(Debug)]
#[derive(Copy)]
#[derive(Clone)]
struct NdIndex (usize, usize);

impl NdIndex {
    fn flatten(self, shape: (usize, usize)) -> usize {
        return self.0 * shape.1 + self.1;
    }
    
    fn from_flat(shape: (usize, usize), flat_idx: usize) -> Self {
        return Self (
            flat_idx.div_euclid(shape.0),
            flat_idx.rem_euclid(shape.0),
        );
    }
    
    fn isin(&self, shape: (usize, usize)) -> bool {
        return self.0 <= shape.0 && self.1 <= shape.1;
    }
    
    fn euclid_distance(&self, other: Self) -> i32 {
        let d = ((other.0 as i32) - (self.0 as i32)).pow(2)
            + ((other.1 as i32) - (self.1 as i32)).pow(2);
        return (d as f32).sqrt().round() as i32;
    }
}

#[derive(Debug)]
struct NdArray {
    shape: (usize, usize),
    data: Vec<i32>,
}

impl NdArray {
    fn zero(shape: (usize, usize)) -> Self {
        let n = shape.0 * shape.1;
        let data = vec![0; n];
        return Self {shape: shape, data: data};
    }
    
    fn fill(&mut self, value: i32) {
        let n = self.shape.0 * self.shape.1;
        for i in 0..n {
            self.data[i] = value;
        }
    }
    
    fn update(&mut self, idx: NdIndex, value: i32) {
        if !idx.isin(self.shape) {
            panic!("idx {:?} not in shape {:?}", idx, self.shape);
        } else {
            let i = idx.flatten(self.shape);
            self.data[i] = value;
        }
    }
}

fn convert_char_to_int(c: char) -> i32 {
    if c.is_digit(36) {
        return c.to_digit(36).expect("") as i32;
    } else {
        panic!("{} is not a recognized digit.", c)
    }
}

fn convert_int_to_char(i: i32) -> String {
    return char::from_digit(i.max(0).min(35) as u32, 36)
        .expect("")
        .to_uppercase()
        .to_string();
}

fn euclid_distance_flood(arr: &mut NdArray, idx: NdIndex, radius: i32) {
    for i in 0..arr.shape.0 {
        for j in 0..arr.shape.1 {
            let p = NdIndex(i, j);
            let b = (radius - p.euclid_distance(idx)).max(0);
            let v = arr.data[p.flatten(arr.shape)] + b;
            arr.update(p, v);
        }
    }
}

fn ndarray_to_string(arr: &NdArray) -> String {
    let mut s = String::from("");
    for i in 0..arr.shape.0 {
        for j in 0..arr.shape.1 {
            let idx = NdIndex(i, j).flatten(arr.shape);
            let b = arr.data[idx];
            s += &convert_int_to_char(b);
        }
        if i < arr.shape.0-1 {
            s += "\n";
        }
    }
    return s;
}

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let h = parse_input!(input_line, i32);
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let w = parse_input!(input_line, i32);

    let mut arr: NdArray = NdArray::zero((h as usize, w as usize));
    for x in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let s = input_line.trim_matches('\n').to_string();
        for (y, v) in s.chars().enumerate() {
            match v {
                '.' => (),
                '\n' => (),
                r => {
                    let idx = NdIndex(x, y);
                    let radius = convert_char_to_int(r);
                    euclid_distance_flood(&mut arr, idx, radius);
                },
            }
        }
    }

    // Write an answer using println!("message...");
    // To debug: eprintln!("Debug message...");

    println!("{}", ndarray_to_string(&arr));
}