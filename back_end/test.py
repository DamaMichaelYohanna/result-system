def generate_hamming_code(data_bits):
    n = len(data_bits)
    m = 4  # Number of check bits

    # Calculate the number of check bits required
    while 2 ** m < n + m + 1:
        m += 1

    # Generate Hamming code
    hamming_code = [0] * (n + m)
    j = 0  # Index for data bits
    k = 0  # Index for Hamming code

    for i in range(1, n + m + 1):
        if i == 2 ** k:
            k += 1
        else:
            hamming_code[i - 1] = data_bits[j]
            #11000101100
            j += 1

    # Calculate and set check bits
    for i in range(m):
        check_bit_idx = 2 ** i - 1
        parity = 0
        for j in range(2 ** i - 1, n + m, 2 ** (i + 1)):
            for k in range(2 ** i):
                if j + k < n + m:
                    parity ^= hamming_code[j + k]
        hamming_code[check_bit_idx] = parity

    return hamming_code


def correct_error(hamming_code):
    m = 1  # Number of check bits
    n = len(hamming_code) - m

    error_bit = 0
    for i in range(m):
        check_bit_idx = 2 ** i - 1
        parity = 0
        for j in range(2 ** i - 1, n + m, 2 ** (i + 1)):
            for k in range(2 ** i):
                if j + k < n + m:
                    parity ^= hamming_code[j + k]
        if parity != hamming_code[check_bit_idx]:
            error_bit += check_bit_idx + 1

    if error_bit != 0:
        hamming_code[error_bit - 1] ^= 1

    corrected_data_bits = [hamming_code[i] for i in range(n) if i != error_bit - 1]

    return corrected_data_bits


def main():
    data_bits = input("Enter data bits (0s and 1s): ")
    data_bits = list(map(int, data_bits))

    hamming_code = generate_hamming_code(data_bits)
    print("Generated Hamming Code:", hamming_code)

    error_position = int(input("Enter error position (0-indexed): "))
    hamming_code[error_position] = 1 - hamming_code[error_position]

    corrected_data_bits = correct_error(hamming_code)
    print("Corrected Data Bits:", corrected_data_bits)


if __name__ == "__main__":
    main()
