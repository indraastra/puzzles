use std::env;
use synacor::vm::{Address, Vm, VmError};

fn main() -> Result<(), VmError> {
  let args: Vec<String> = env::args().collect();
  let filename = &args[1];
  let address: u16 = if args.len() >= 3 {
    args[2].parse().unwrap_or(0)
  } else {
    0
  };

  let mut vm = Vm::default();
  let n_instructions = vm.load_memory(filename)?;
  println!("Loaded {} instructions from {}", n_instructions, filename);
  // From teleport.rs: Found z = 25734 satisfying ackish(4, 1, z) == 6
  vm.registers[7] = 25734;
  for a in 5489..=5497 {
    vm.memory[a] = 21;
  }
  println!("Starting execution at {}...\n\n\n", address);
  let mut input = std::io::stdin();
  let mut output = std::io::stdout();
  let cycles = vm.run(&mut input, &mut output, Address::Offset(address))?;
  println!("Executed {} instructions", cycles);

  Ok(())
}
