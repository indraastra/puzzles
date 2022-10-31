use std::fs;

use crate::vm::VmError;

/// Reads `buf_in` as a sequence of unsigned little-endian 16-bit values,
/// stores them in `buf_out`, and returns the number of values read.
pub fn u8_to_u16_le_bytes(buf_in: &[u8], buf_out: &mut [u16]) -> Result<usize, VmError> {
    if buf_in.len() % 2 != 0 {
        return Err(VmError::ProgramMisaligned(buf_in.len()));
    }

    let (chunks, _remainder) = buf_in.as_chunks();
    if chunks.len() > buf_out.len() {
        Err(VmError::ProgramTooLarge(chunks.len()))
    } else {
        for (i, [lo, hi]) in chunks.iter().enumerate() {
            if i > buf_out.len() {
                break;
            }
            buf_out[i] = u16::from_le_bytes([*lo, *hi]);
        }
        Ok(buf_in.len() / 2)
    }
}

/// Reads `buf_in` as a sequence of 16-bit values and returns them as 8-bit little-endian bytes.
pub fn u16_to_u8_le_bytes(buf_in: &[u16]) -> Result<Vec<u8>, VmError> {
    Ok(buf_in.iter().flat_map(|n| n.to_le_bytes()).collect())
}

pub fn read_binary_file(filename: &str) -> Result<Vec<u8>, VmError> {
    Ok(fs::read(filename)?)
}

pub fn write_binary_file(bytes: &[u8], filename: &str) -> Result<usize, VmError> {
    fs::write(filename, bytes)?;
    Ok(bytes.len())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::vm::VmError;

    #[test]
    fn to_u16_bytes_too_small_buf() {
        let mut too_small_buf = [0u16; 1];
        assert_eq!(
            u8_to_u16_le_bytes(&[0, 1, 2, 3], &mut too_small_buf),
            Err(VmError::ProgramTooLarge(2))
        );
    }

    #[test]
    fn to_u16_bytes_bad_alignment() {
        let mut buf_out = [0u16; 4];
        assert_eq!(
            u8_to_u16_le_bytes(&[0, 1, 2], &mut buf_out),
            Err(VmError::ProgramMisaligned(3))
        );
    }

    #[test]
    fn to_u16_bytes_counts() {
        let mut buf_out = [0u16; 4];
        assert_eq!(u8_to_u16_le_bytes(&[], &mut buf_out), Ok(0));
        assert_eq!(u8_to_u16_le_bytes(&[0, 0, 0, 0], &mut buf_out), Ok(2));
    }

    #[test]
    fn to_u16_bytes_values() {
        let mut buf_out = [0u16; 4];
        assert_eq!(u8_to_u16_le_bytes(&[0x34, 0x12], &mut buf_out), Ok(1));
        assert_eq!(buf_out[0], 0x1234);

        assert_eq!(
            u8_to_u16_le_bytes(
                &[0x34, 0x12, 0x01, 0xFF, 0x12, 0x34, 0xFF, 0x01],
                &mut buf_out
            ),
            Ok(4)
        );
        assert_eq!(buf_out, [0x1234, 0xFF01, 0x3412, 0x01FF]);
    }

    #[test]
    fn to_u8_bytes_values() {
        assert_eq!(
            u16_to_u8_le_bytes(&[0x3421, 0x1234]),
            Ok(vec![0x21, 0x34, 0x34, 0x12])
        );
    }
}
