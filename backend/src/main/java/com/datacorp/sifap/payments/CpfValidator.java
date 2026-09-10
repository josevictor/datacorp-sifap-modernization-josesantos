package com.datacorp.sifap.payments;

final class CpfValidator {

    private CpfValidator() {
    }

    static boolean isValid(String cpf) {
        if (cpf == null || !cpf.matches("\\d{11}") || cpf.chars().distinct().count() == 1) {
            return false;
        }

        int firstDigit = digit(cpf, 9, 10);
        int secondDigit = digit(cpf, 10, 11);

        return firstDigit == Character.digit(cpf.charAt(9), 10)
            && secondDigit == Character.digit(cpf.charAt(10), 10);
    }

    private static int digit(String cpf, int length, int initialWeight) {
        int sum = 0;
        for (int index = 0; index < length; index++) {
            sum += Character.digit(cpf.charAt(index), 10) * (initialWeight - index);
        }
        int remainder = (sum * 10) % 11;
        return remainder == 10 ? 0 : remainder;
    }
}
