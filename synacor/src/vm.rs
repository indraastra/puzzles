use std::{
    error::Error,
    fmt::{Display, Formatter},
    io,
};

use crate::parser::{read_binary_file, read_u16_le_bytes};

const MAX_LITERAL: u16 = u16::MAX >> 1;
const MAX_REGISTER: u16 = MAX_LITERAL + 8;
const RAM_SIZE: usize = MAX_LITERAL as usize;
const REG_SIZE: usize = 8;

#[derive(Debug, PartialEq)]
#[non_exhaustive]
pub enum VmError {
    ProgramTooLarge(usize),
    ProgramMisaligned(usize),
    IoError(String),
    UnhandledInstruction(u16),
    EmptyStack,
    EmptyInput,
}

impl Display for VmError {
    fn fmt(&self, f: &mut Formatter) -> std::fmt::Result {
        use VmError::*;
        match &self {
            ProgramTooLarge(i_size) => {
                write!(
                    f,
                    "program has {} instructions; too large for memory of {}",
                    i_size, RAM_SIZE
                )
            }
            ProgramMisaligned(b_size) => {
                write!(f, "program has {} bytes; not aligned to u16", b_size)
            }
            IoError(error) => {
                write!(f, "io error: {}", error)
            }
            UnhandledInstruction(op) => {
                write!(f, "unhandled instruction: {}", op)
            }
            EmptyStack => {
                write!(f, "tried to pop an empty stack")
            }
            EmptyInput => {
                write!(f, "tried to read from an empty input")
            }
        }
    }
}

impl Error for VmError {}

impl From<io::Error> for VmError {
    fn from(value: io::Error) -> Self {
        Self::IoError(value.to_string())
    }
}

#[derive(Debug)]
pub struct Vm {
    pub memory: [u16; RAM_SIZE],
    pub registers: [u16; REG_SIZE],
    pub stack: Vec<u16>,
}

impl Default for Vm {
    fn default() -> Self {
        Self {
            memory: [0; RAM_SIZE],
            registers: [0; REG_SIZE],
            stack: vec![],
        }
    }
}

impl Vm {
    /// Loads `instructions` into memory and starts executing them.
    pub fn load_instructions(&mut self, instructions: &[u16]) -> Result<usize, VmError> {
        let size = instructions.len();
        if size > self.memory.len() {
            Err(VmError::ProgramTooLarge(size))
        } else {
            self.memory[..size].copy_from_slice(instructions);
            Ok(size)
        }
    }

    /// Loads little-endian u16 values from `filename` as instructions into memory and starts executing them.
    pub fn load_program(&mut self, filename: &str) -> Result<usize, VmError> {
        let bytes = read_binary_file(filename)?;
        read_u16_le_bytes(&bytes, &mut self.memory)
    }

    /// Executed the instructions in memory and returns the number of cycles spent until halting.
    pub fn run(
        &mut self,
        input: &mut impl io::Read,
        output: &mut impl io::Write,
    ) -> Result<usize, VmError> {
        let mut pc = 0;
        let mut cycles = 0;
        loop {
            match self.read(pc) {
                // halt: 0
                //   stop execution and terminate the program
                0 => break,
                1 => {
                    // set: 1 a b
                    //   set register <a> to the value of <b>
                    let (a, b) = self.read2(pc + 1);
                    self.load(a, self.eval(b));
                    pc += 3;
                }
                2 => {
                    // push: 2 a
                    //   push <a> onto the stack
                    let a = self.read(pc + 1);
                    self.stack.push(self.eval(a));
                    pc += 2;
                }
                3 => {
                    // pop: 3 a
                    //   remove the top element from the stack and write it into <a>; empty stack = error
                    let a = self.read(pc + 1);
                    if let Some(v) = self.stack.pop() {
                        self.load(a, v);
                        pc += 2;
                    } else {
                        return Err(VmError::EmptyStack);
                    }
                }
                cmp @ 4..=5 => {
                    let (a, b, c) = self.read3(pc + 1);
                    let b = self.eval(b);
                    let c = self.eval(c);
                    // eq: 4 a b c
                    //   set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
                    // gt: 5 a b c
                    //   set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
                    if (cmp == 4 && b == c) || (cmp == 5 && b > c) {
                        self.load(a, 1)
                    } else {
                        self.load(a, 0)
                    }
                    pc += 4;
                }
                6 => {
                    // jmp: 6 a
                    //   jump to <a>
                    let a = self.read(pc + 1);
                    pc = self.eval(a);
                }
                7 => {
                    // jt: 7 a b
                    //   if <a> is nonzero, jump to <b>
                    let (a, b) = self.read2(pc + 1);
                    if self.eval(a) != 0 {
                        pc = self.eval(b);
                    } else {
                        pc += 3;
                    }
                }
                8 => {
                    // jf: 8 a b
                    //   if <a> is zero, jump to <b>
                    let (a, b) = self.read2(pc + 1);
                    if self.eval(a) == 0 {
                        pc = self.eval(b);
                    } else {
                        pc += 3;
                    }
                }
                op @ 9..=13 => {
                    let (a, b, c) = self.read3(pc + 1);
                    let b = self.eval(b);
                    let c = self.eval(c);
                    // add: 9 a b c
                    //   assign into <a> the sum of <b> and <c> (modulo 32768)
                    // mult: 10 a b c
                    //   store into <a> the product of <b> and <c> (modulo 32768)
                    // mod: 11 a b c
                    //   store into <a> the remainder of <b> divided by <c>
                    // and: 12 a b c
                    //   stores into <a> the bitwise and of <b> and <c>
                    // or: 13 a b c
                    //   stores into <a> the bitwise or of <b> and <c>
                    let result = match op {
                        9 => u16::wrapping_add(b, c),
                        10 => u16::wrapping_mul(b, c),
                        11 => b % c,
                        12 => b & c,
                        13 => b | c,
                        _ => unreachable!(),
                    };
                    self.load(a, result & MAX_LITERAL);
                    pc += 4;
                }
                14 => {
                    // not: 14 a b
                    //   stores 15-bit bitwise inverse of <b> in <a>
                    let (a, b) = self.read2(pc + 1);
                    self.load(a, !self.eval(b) & MAX_LITERAL);
                    pc += 3;
                }
                15 => {
                    // rmem: 15 a b
                    //   read memory at address <b> and write it to <a>
                    let (a, b) = self.read2(pc + 1);
                    self.load(a, self.read(self.eval(b)));
                    pc += 3;
                }
                16 => {
                    // wmem: 16 a b
                    //   write the value from <b> into memory at address <a>
                    let (a, b) = self.read2(pc + 1);
                    self.store(self.eval(a), self.eval(b));
                    pc += 3;
                }
                17 => {
                    // call: 17 a
                    //   write the address of the next instruction to the stack and jump to <a>
                    let a = self.read(pc + 1);
                    self.stack.push(pc + 2);
                    pc = self.eval(a);
                }
                18 => {
                    // ret: 18
                    //   remove the top element from the stack and jump to it; empty stack = halt
                    if let Some(v) = self.stack.pop() {
                        pc = v;
                    } else {
                        break;
                    }
                }
                19 => {
                    // out: 19 a
                    //   write the character represented by ascii code <a> to the terminal
                    let a = self.read(pc + 1);
                    output.write(&[self.eval(a) as u8])?;
                    pc += 2;
                }
                20 => {
                    // in: 20 a
                    //   read a character from the terminal and write its ascii code to <a>
                    let a = self.read(pc + 1);
                    let mut buf = [0; 1];
                    input.read(&mut buf)?;
                    self.load(a, buf[0] as u16);
                    pc += 2;
                }
                // noop: 21
                //   no operation
                21 => pc += 1,
                op => return Err(VmError::UnhandledInstruction(op)),
            }
            cycles += 1;
            // dbg!(&self.registers);
            // dbg!(&self.stack);
        }
        Ok(cycles)
    }

    /// Evaluates `a` by returning it as-is if it is a literal, or retrieving its value from register.
    fn eval(&self, a: u16) -> u16 {
        if is_literal(a) {
            a
        } else if is_register(a) {
            self.registers[register_num(a)]
        } else {
            panic!("invalid value {} is neither a literal nor a register!", a);
        }
    }
    /// Loads the value `v` into register `a`.
    fn load(&mut self, a: u16, v: u16) {
        if is_register(a) {
            self.registers[register_num(a)] = v;
        } else {
            panic!("invalid value {} for register!", a);
        }
    }

    /// Stores the value `v` at memory address `a`.
    fn store(&mut self, a: u16, v: u16) {
        if is_literal(a) {
            self.memory[a as usize] = v;
        } else {
            panic!("invalid value {} for address!", a);
        }
    }

    /// Loads the value(s) starting at memory address `a`.
    fn read(&self, a: u16) -> u16 {
        if let Some(&v) = self.memory.get(a as usize) {
            v
        } else {
            panic!("reading address past end of memory: {}", a)
        }
    }
    fn read2(&self, a: u16) -> (u16, u16) {
        (self.read(a), self.read(a + 1))
    }
    fn read3(&self, a: u16) -> (u16, u16, u16) {
        (self.read(a), self.read(a + 1), self.read(a + 2))
    }
}

fn is_literal(v: u16) -> bool {
    v <= MAX_LITERAL
}

fn is_register(v: u16) -> bool {
    MAX_LITERAL < v && v <= MAX_REGISTER
}

fn register_num(v: u16) -> usize {
    (v & 0x7) as usize
}

#[cfg(test)]
mod tests {
    use super::*;

    fn register_val(n: usize) -> u16 {
        MAX_LITERAL + 1 + (n as u16)
    }

    #[test]
    fn check_literals() {
        assert!(is_literal(0));
        assert!(is_literal(0xFF));
        assert!(is_literal(MAX_LITERAL));
        assert!(!is_literal(MAX_LITERAL + 1));
        assert!(!is_literal(u16::MAX));
    }

    #[test]
    fn check_registers() {
        assert!(!is_register(0));
        assert!(!is_register(0xFF));
        assert!(!is_register(MAX_LITERAL));
        for n in 0..=7usize {
            let r = register_val(n);
            assert_eq!(register_num(r), n);
            assert!(is_register(r));
        }
        assert!(!is_register(u16::MAX));
    }

    #[test]
    fn executes_simple_program() {
        let mut vm = Vm::default();
        // - The program "9,32768,32769,4,19,32768" occupies six memory addresses and should:
        //   - Store into register 0 the sum of 4 and the value contained in register 1.
        //   - Output to the terminal the character with the ascii code contained in register 0.
        assert_eq!(
            vm.load_instructions(&[9, 32768, 32768, 4, 19, 32768]),
            Ok(6)
        );

        let mut input: &[u8] = b"";
        let mut output: Vec<u8> = Vec::new();
        vm.run(&mut input, &mut output)
            .expect("error executing simple program!");
        assert_eq!(vm.eval(register_val(0)), 4);
        assert_eq!(output, vec![4]);
    }
}
