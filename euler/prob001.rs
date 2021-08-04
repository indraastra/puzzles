fn main() {
    let mut total = 0u32;

    for n in 1..1000 {
        if n % 3 == 0 || n % 5 == 0 {
            total += n
        }
    }
    println!("{}", total)
}

