#include <cmath>
#include <string>
#include <cstdio>
#include <iostream>
#include <vector>
#include <map>
#include <fstream>

#define COUNT_NORMAL_BITS 6
#define COUNT_CHECK_BITS 4

#define FILE_INPUT "../../files/4/input.txt"
#define FILE_BINARY "../../files/4/encoded.bin"
#define FILE_OUTPUT "../../files/4/output.txt"

// Флаг чётности
bool flag = false;

// Функция осуществляет конвертацию из 10 в 2
void dec_into_bin(int dec, size_t size, int *ar) {
    for (int i = 0; i < size; i++) {
        ar[i] = 0;
    }

    // Размер нашего блока с данными
    size_t k = size - 1;
    while (dec > 1) {
        ar[k] = dec % 2;
        dec = floor(dec / 2);
        k--;
    }

    // Флаг чётности - если 1, то чётное, если 0 - не чётное. По умолчанию стоит 0
    if (flag) {
        ar[k] = 1;
    }
    flag = true;
}

// Подсчёт количества проверочных битов
int amount_check_bits(size_t size) {
    int k = 2;
    while (k < log(k + size + 1) / log(2)) {
        k++;
    }
    return k;
}

// Инверсия битов
int inverse(int k) {
    return k == 0;
}

void display_results_to_console(std::map<char, std::vector <short int>> &data_to_display, size_t size_number) {
    // Вывод таблицы: символ - код (без контрольный битов)
    for (auto & iter : data_to_display) {
        std::cout << "Symbol: " << iter.first << "\tCharacter code : ";
        for (size_t i = 0; i < size_number; i++) {
            std::cout << iter.second[i];
        }
        std::cout << std::endl;
    }
}

// Помехоустойчивый кодер
void encode(std::ifstream &file, std::map<char, std::vector <short int>> &table) {
    std::ofstream g(FILE_BINARY, std::ios::out | std::ios::binary);

    std::vector<int> check(COUNT_CHECK_BITS);
    while (true) {
        char c = file.get();
        if (file.eof()) {
            break;
        }

        std::vector<short int> x = table[c];

        // Таким образом осуществляется помехоустойчивость
        check[0] = x[0] ^ x[1] ^ x[3] ^ x[4];
        check[1] = x[0] ^ x[2] ^ x[3] ^ x[5];
        check[2] = x[1] ^ x[2] ^ x[3];
        check[3] = x[4] ^ x[5];

        // Записываем в файл
        g << check[0] << check[1] << x[0] << check[2];
        for (int i = 1; i < 4; i++) {
            g << x[i];
        }

        g << check[3] << x[4] << x[5];
    }

    g.close();
}

// Метод, который осуществляет обратную операцию - декодирование
void decode(std::map<char, std::vector <short int>> &table, bool enable_noise) {
    std::ifstream encoded_file(FILE_BINARY, std::ios:: in | std::ios::binary);
    std::ofstream output_file(FILE_OUTPUT, std::ios::out);

    std::vector <int> encoded_data(COUNT_NORMAL_BITS + COUNT_NORMAL_BITS);
    std::vector <int> mis(COUNT_CHECK_BITS);
    std::vector <int> result_decoding(COUNT_NORMAL_BITS);

    int amount_errors = 0;
    int amount_fixed_errors = 0;
    int amount_non_fixed_errors = 0;

    double noise;

    // Вероятность инверсии символа (имитация шума)
    const double ver = 0.9;
    int last_bits;

    while (true) {
        int index = -1;
        for (int i = 0; i < COUNT_NORMAL_BITS + COUNT_CHECK_BITS; i++) {
            char c = encoded_file.get();

            if (c == '0') {
                encoded_data[i] = 0;
            } else {
                encoded_data[i] = 1;
            }

            // Добавление шума при помощи вероятностного метода
            noise = (1 + rand() % 100) / 100;
            if (noise > ver and enable_noise) {
                encoded_data[i] = inverse(encoded_data[i]);
                ++amount_errors;
            }
        }

        for (int i = 0; i < COUNT_CHECK_BITS; i++) {
            mis[i] = 0;
        }
        if (encoded_data[0] ^ encoded_data[2] ^ encoded_data[4] ^ encoded_data[6] ^ encoded_data[8] != 0) {
            mis[0] = 1;
        }
        if (encoded_data[1] ^ encoded_data[2] ^ encoded_data[5] ^ encoded_data[6] ^ encoded_data[9] != 0) {
            mis[1] = 1;
        }
        if (encoded_data[3] ^ encoded_data[4] ^ encoded_data[5] ^ encoded_data[6] != 0) {
            mis[2] = 1;
        }
        if (encoded_data[7] ^ encoded_data[8] ^ encoded_data[9]) {
            mis[3] = 1;
        }

        if (mis[0] + mis[1] + mis[2] + mis[3] == 0) {
            index = -5;
        } else if ((mis[0] == 0) && (mis[1] == 0)) {
            index = 3;
        } else if ((mis[0] == 0) && (mis[2] == 0) && (mis[3] == 0)) {
            index = 1;
        } else if ((mis[0] == 0) && (mis[2] == 0) && (mis[1] == 0)) {
            index = 9;
        } else if ((mis[1] == 0) && (mis[2] == 0) && (mis[3] == 0)) {
            index = 8;
        } else if ((mis[1] == 0) && (mis[2] == 0) && (mis[0] == 0)) {
            index = 7;
        } else if ((mis[2] == 0) && (mis[1] == 0) && (mis[3] == 0)) {
            index = 0;
        } else if ((mis[2] == 0) && (mis[3] == 0)) {
            index = 2;
        } else if (mis[3] == 0) {
            index = 6;
        } else if ((mis[0] == 0) && (mis[3] == 0)) {
            index = 5;
        } else if ((mis[1] == 0) && (mis[3] == 0)) {
            index = 4;
        }

        if (index > 0) {
            encoded_data[index] = inverse(encoded_data[index]);
            ++amount_fixed_errors;
        }

        // Декодировка
        result_decoding[0] = encoded_data[2];
        result_decoding[1] = encoded_data[4];
        result_decoding[2] = encoded_data[5];
        result_decoding[3] = encoded_data[6];
        result_decoding[4] = encoded_data[8];
        result_decoding[5] = encoded_data[9];

        // Процесс преобразования из числа в символ
        for (auto & iter : table) {
            last_bits = 0;
            for (int i = 0; i < COUNT_NORMAL_BITS; i++) {
                if (iter.second[i] == result_decoding[i]) {
                    last_bits++;
                }
            }

            if (last_bits == COUNT_NORMAL_BITS) {
                output_file << iter.first;
            }
        }

        if (encoded_file.eof()) {
            break;
        }
    }

    // Закрываем файлы
    encoded_file.close();
    output_file.close();

    std::cout << "Count errors: " << amount_errors << std::endl;
    std::cout << "Count fixed errors: " << amount_fixed_errors << std::endl;
    std::cout << "Count non fixed errors: " << amount_errors - amount_fixed_errors << std::endl;
}

// Метод, который формирует индивидуальный код для каждого числа
std::map<char, std::vector <short int>> get_table(size_t size_number, std::map<char, int> &table_with_frequency_symbols) {
    int count = 0;

    // Представление данного блока в памяти происходит на основании вектора из short-ов
    std::vector <short int> code;
    int *ar = new int[size_number];

    // Таблица символ - его код (6-ти значный, в двоичном виде)
    std::map<char, std::vector <short int>> table;
    for (auto & table_with_frequency_symbol : table_with_frequency_symbols) {
        if (table_with_frequency_symbol.second) {
            dec_into_bin(count, size_number, ar);
            // Если нашёлся нужный нам символ, то в этом случае очищаем вектор
            code.clear();

            // И пересоздаём его, поскольку нам нужно записать двоичный код
            for (int i = 0; i < size_number; i++) {
                code.push_back(ar[i]);
            }

            table[table_with_frequency_symbol.first] = code;
            ++count;
        }
    }

    return table;
}

// Данная функция осуществляет подсчёт 0 и 1 в файле
std::pair<int, int> calculate_zeroes_and_ones() {
    int count_zeroes = 0;
    int count_ones = 0;

    std::ifstream file(FILE_BINARY, std::ios::in | std::ios::binary);

    while (!file.eof()) {
        char c = file.get();

        if (!file.eof()) {
            if (c == '0') {
                ++count_zeroes;
            } else {
                ++count_ones;
            }
        }
    }

    file.close();

    return std::make_pair(count_zeroes, count_ones);
}

int main(int argc, char *argv[]) {
    if (remove(FILE_BINARY) ==  1) {
        std::cout << "Success remove the old binary file\n";
    }

    if (remove(FILE_OUTPUT) == 1) {
        std::cout << "Success remove the old output file\n";
    }

    std::ifstream f(FILE_INPUT, std::ios::in);

    // Вычисление размера алфавита, количество информационных битов, количество проверочных битов,
    // Таблица, где хранятся биты с данными
    std::map<char, int> table_with_frequency_symbols;

    // Количество символов в исходном файле (может быть очень большим)
    long k = 0;

    while (!f.eof()) {
        char c = f.get();

        if (!f.eof()) {
            ++table_with_frequency_symbols[c];
            ++k;
        }
    }

    //Блок: длина блока 10 символов: из них 6 информационные и 4 проверочные.
    int size_symbol = 55;
    size_t size_frequency_table = table_with_frequency_symbols.size();

    // Вычисляется длина кодового слова (логарифмическая формула Шеннона)
    size_t size_number = ceil(log(size_symbol) / log(2));
    size_t count_bits = amount_check_bits(size_number);

    std::cout << "Size one symbol: " << size_number << "\tCount check bits: " << count_bits << std::endl;
    std::cout << "Size frequency table: " << size_frequency_table << std::endl;

    std::map<char, std::vector <short int>> table = get_table(size_number, table_with_frequency_symbols);

    display_results_to_console(table, size_number);

    // Очищаем ошибки и сдвигаем дескриптор в начало
    f.clear();
    f.seekg(0);

    // Осуществляем запись в файл
    encode(f, table);
    f.close();

    // Осуществляем декодирование данных
    decode(table, true);

    std::pair<int, int> numbers = calculate_zeroes_and_ones();

    std::cout << "Count symbols: " << numbers.first + numbers.second << std::endl;
    std::cout << "Count '0': " << numbers.first << "\nCount '1': " << numbers.second << std::endl;
    std::cout << "Average number of binary characters, which was needed to transfer 1 letter: " <<
    (numbers.first + numbers.second) / k << std::endl;

    return EXIT_SUCCESS;
}