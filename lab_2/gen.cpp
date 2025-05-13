#include <iostream>
#include <fstream>
#include <bitset>
#include <random>
#include <string>

std::bitset<128> generateRandomSequence() {
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_int_distribution<uint64_t> dis(0, UINT64_MAX);

    std::bitset<128> result;
    for (int i = 0; i < 2; ++i) {
        result |= (std::bitset<128>(dis(gen)) << (i * 64));
    }

    return result;
}

void saveBitsetToFile(const std::string& filename, const std::bitset<128>& bits) {
    std::ofstream file(filename);
    if (file) {
        file << bits.to_string();
        file.close();
    }
    else {
        std::cerr << "Ошибка при открытии файла для записи: " << filename << std::endl;
    }
}

int main() {
    setlocale(LC_ALL, "RU");
    std::bitset<128> randomSequence = generateRandomSequence();
    std::cout << "Случайная 128-битная последовательность: " << randomSequence << std::endl;
    saveBitsetToFile("cpp_sequence.txt", randomSequence);
    return 0;
}