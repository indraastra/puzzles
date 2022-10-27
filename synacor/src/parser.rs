use std::fs;

use crate::vm::VmError;

/// Reads `buf_in` as a sequence of unsigned little-endian 16-bit values,
/// stores them in `buf_out`, and returns the number of values read.
pub fn read_u16_le_bytes(buf_in: &[u8], buf_out: &mut [u16]) -> Result<usize, VmError> {
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

pub fn read_binary_file(filename: &str) -> Result<Vec<u8>, VmError> {
    Ok(fs::read(filename)?)
}

#[cfg(test)]
mod tests {
    use super::read_u16_le_bytes;
    use crate::vm::VmError;

    #[test]
    fn read_u16_bytes_too_small_buf() {
        let mut too_small_buf = [0u16; 1];
        assert_eq!(
            read_u16_le_bytes(&[0, 1, 2, 3], &mut too_small_buf),
            Err(VmError::ProgramTooLarge(2))
        );
    }

    #[test]
    fn read_u16_bytes_bad_alignment() {
        let mut buf_out = [0u16; 4];
        assert_eq!(
            read_u16_le_bytes(&[0, 1, 2], &mut buf_out),
            Err(VmError::ProgramMisaligned(3))
        );
    }

    #[test]
    fn read_u16_bytes_counts() {
        let mut buf_out = [0u16; 4];
        assert_eq!(read_u16_le_bytes(&[], &mut buf_out), Ok(0));
        assert_eq!(read_u16_le_bytes(&[0, 0, 0, 0], &mut buf_out), Ok(2));
    }

    #[test]
    fn read_u16_bytes_values() {
        let mut buf_out = [0u16; 4];
        assert_eq!(read_u16_le_bytes(&[0x34, 0x12], &mut buf_out), Ok(1));
        assert_eq!(buf_out[0], 0x1234);

        assert_eq!(
            read_u16_le_bytes(
                &[0x34, 0x12, 0x01, 0xFF, 0x12, 0x34, 0xFF, 0x01],
                &mut buf_out
            ),
            Ok(4)
        );
        assert_eq!(buf_out, [0x1234, 0xFF01, 0x3412, 0x01FF]);
    }
}
