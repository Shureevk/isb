import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Main {
    public static final int BIT_LENGTH = 128;

    public static String generateRandomSequence(int length) {
        Random random = new Random();
        StringBuilder binaryString = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            binaryString.append(random.nextBoolean() ? '1' : '0');
        }
        return binaryString.toString();
    }

    public static void saveToFile(String filename, String data) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(data);
            System.out.println("Sequence saved to " + filename);
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String sequence = generateRandomSequence(BIT_LENGTH);
        System.out.println("Случайная " + BIT_LENGTH + "-битная бинарная последовательность: " + sequence);
        saveToFile("java_sequence.txt", sequence);
    }
}
