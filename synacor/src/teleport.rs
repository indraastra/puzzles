use indicatif::ParallelProgressIterator;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};

use std::collections::HashMap;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Registers {
  a: u16,
  b: u16,
  z: u16,
}

fn ackish(rs: Registers, cache: &mut HashMap<Registers, u16>) -> u16 {
  if let Some(&v) = cache.get(&rs) {
    return v;
  }
  let v = match rs {
    Registers { a: 0, b, z: _ } => (b + 1) & 0x7FFF,
    Registers { a, b: 0, z } => ackish(Registers { a: a - 1, b: z, z }, cache),
    Registers { a, b, z } => {
      let b = ackish(Registers { a, b: b - 1, z }, cache);
      ackish(Registers { a: a - 1, b, z }, cache)
    }
  };
  cache.insert(rs, v);
  v
}

fn main() {
  let pool = rayon::ThreadPoolBuilder::new()
    .num_threads(16)
    .stack_size(8 * 1024 * 1024)
    .build()
    .unwrap();

  pool.install(|| {
    let zs: Vec<u16> = (0..32768).collect();
    match zs
      .par_iter()
      .progress_count(zs.len() as u64)
      .find_any(|&&z| {
        let mut cache = Box::new(HashMap::new());
        ackish(Registers { a: 4, b: 1, z }, &mut cache) == 6
      }) {
      Some(z) => println!("Found z = {} satisfying ackish(4, 1, z) == 6", z),
      None => println!("Failed to find a z satisfying ackish(4, 1, z) == 6"),
    }
  });
}
