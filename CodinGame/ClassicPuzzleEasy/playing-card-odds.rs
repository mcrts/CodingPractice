use std::io;
use std::char;
use std::collections::HashSet;
use std::hash::{Hash, Hasher};

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

fn rank_keys() -> HashSet<char> {
    return HashSet::from(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']);
}
fn suit_keys() -> HashSet<char> {
    return HashSet::from(['C', 'D', 'H', 'S']);
}

#[derive(Debug)]
#[derive(Eq, PartialEq)]
struct Card {
    rank: char,
    suit: char,
}
impl Hash for Card {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.rank.hash(state);
        self.suit.hash(state);
    }
}

#[derive(Debug)]
struct DescriptiveClassification {
    ranks: HashSet<char>,
    suits: HashSet<char>,
}

impl DescriptiveClassification {
    fn from_string(s: String) -> Self {
        let RANKS: HashSet<char> = rank_keys();
        let SUITS: HashSet<char> = suit_keys();

        let mut ranks: HashSet<char> = HashSet::new();
        let mut suits: HashSet<char> = HashSet::new();

        for c in s.chars() { 
            if RANKS.contains(&c) {
                ranks.insert(c);
            }
            if SUITS.contains(&c) {
                suits.insert(c);
            }
        }

        return DescriptiveClassification {
            ranks: ranks,
            suits: suits,
        };
    }
    fn empty() -> Self {
        return Self::from_string("".to_string());
    }
    fn full_deck() -> HashSet<Card> {
        return Self::empty().cards()
    }
    fn cards(&self) -> HashSet<Card> {
        let RANKS: HashSet<char> = rank_keys();
        let SUITS: HashSet<char> = suit_keys();

        let ranks: &HashSet<char>;
        if self.ranks.is_empty() {
            ranks = &RANKS;
        } else {
            ranks = &self.ranks;
        }
        let suits: &HashSet<char>;
        if self.suits.is_empty() {
            suits = &SUITS;
        } else {
            suits = &self.suits;
        }
        let mut items: HashSet<Card> = HashSet::new();

        for s in suits {
            for r in ranks {
                items.insert(Card{rank: *r, suit: *s});
            }
        }
        return items
    }

}
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let inputs = input_line.split(" ").collect::<Vec<_>>();
    let r = parse_input!(inputs[0], i32);
    let s = parse_input!(inputs[1], i32);

    let mut removed_cards: HashSet<Card> = HashSet::new();
    for i in 0..r as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let removed = input_line.trim_matches('\n').to_string();
        let removed_dc = DescriptiveClassification::from_string(removed);
        for c in removed_dc.cards() {
            removed_cards.insert(c);
        }

    }
    let mut sought_cards: HashSet<Card> = HashSet::new();
    for i in 0..s as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let sought = input_line.trim_matches('\n').to_string();
        let sought_dc = DescriptiveClassification::from_string(sought);
        for c in sought_dc.cards() {
            sought_cards.insert(c);
        }
    }

    let deck: HashSet<Card> = DescriptiveClassification::full_deck();
    let finaldeck = deck.difference(&removed_cards);
    let mut deck_size = 0;
    let mut sought_size = 0;
    for c in finaldeck{
        if sought_cards.contains(c) {
            sought_size += 1;
        }
        deck_size += 1;
    }

    let p: i32 = 100 * sought_size / deck_size;
    //let finalsought = finaldeck.
    // Write an answer using println!("message...");
    // To debug: eprintln!("Debug message...");

    println!("{}%", p);
}
