use std::env;
use synacor::vm::{Vm, VmError};

fn main() -> Result<(), VmError> {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];

    let mut vm = Vm::default();
    let n_instructions = vm.load_program(filename)?;
    println!("Loaded {} instructions from {}", n_instructions, filename);

    println!("Starting execution...");
    let cycles = vm.run(&mut std::io::stdin(), &mut std::io::stdout())?;
    println!("Executed {} instructions", cycles);

    Ok(())
}
