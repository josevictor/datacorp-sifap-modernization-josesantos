package com.datacorp.sifap.shared.exception;

import com.datacorp.sifap.payments.BeneficiaryQueryNotFoundException;
import com.datacorp.sifap.payments.BeneficiaryQueryRejectedException;
import com.datacorp.sifap.payments.BeneficiaryQuerySearchCriteriaException;
import com.datacorp.sifap.payments.PaymentGenerationNotFoundException;
import com.datacorp.sifap.payments.PaymentGenerationRejectedException;
import java.net.URI;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(PaymentGenerationRejectedException.class)
    ProblemDetail handleRejected(PaymentGenerationRejectedException ex) {
        return problem(HttpStatus.UNPROCESSABLE_ENTITY, ex.getMessage());
    }

    @ExceptionHandler(PaymentGenerationNotFoundException.class)
    ProblemDetail handleNotFound(PaymentGenerationNotFoundException ex) {
        return problem(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        return problem(HttpStatus.BAD_REQUEST, "Invalid request");
    }

    @ExceptionHandler(BeneficiaryQueryNotFoundException.class)
    ProblemDetail handleBeneficiaryNotFound(BeneficiaryQueryNotFoundException ex) {
        return problem(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(BeneficiaryQueryRejectedException.class)
    ProblemDetail handleBeneficiaryRejected(BeneficiaryQueryRejectedException ex) {
        return problem(HttpStatus.UNPROCESSABLE_ENTITY, ex.getMessage());
    }

    @ExceptionHandler(BeneficiaryQuerySearchCriteriaException.class)
    ProblemDetail handleSearchCriteria(BeneficiaryQuerySearchCriteriaException ex) {
        return problem(HttpStatus.BAD_REQUEST, ex.getMessage());
    }

    private ProblemDetail problem(HttpStatus status, String detail) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, detail);
        problem.setType(URI.create("https://datacorp.example/problems/payment-generation"));
        return problem;
    }
}
