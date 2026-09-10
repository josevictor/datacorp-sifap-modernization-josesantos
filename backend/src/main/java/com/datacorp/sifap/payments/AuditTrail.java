package com.datacorp.sifap.payments;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * Registro da trilha de acesso a dados pessoais (REQ-042).
 *
 * <p>Espelha o bloco {@code PERSONAL DATA ACCESS TRAIL} de
 * {@code CONSBENF.NSP:168-179}, que cita a IN-TCU 63/2010.
 *
 * <p>O campo legado {@code USR-EVENT} não tem equivalente: não há autenticação
 * nesta feature, então a trilha registra que houve acesso, não por quem.
 */
@Entity
@Table(name = "audit_trail")
class AuditTrail {

    static final String QUERY_ACTION = "CO";
    static final String BENEFICIARY_ENTITY = "BENF";

    @Id
    private UUID id;

    @Column(nullable = false, length = 2)
    private String actionCode;

    @Column(nullable = false, length = 4)
    private String entityType;

    @Column(nullable = false, length = 11)
    private String entityId;

    @Column(nullable = false, length = 11)
    private String affectedCpf;

    @Column(nullable = false, length = 120)
    private String description;

    @Column(nullable = false, length = 10)
    private String moduleCode;

    @Column(nullable = false)
    private OffsetDateTime occurredAt;

    protected AuditTrail() {
    }

    private AuditTrail(String cpf, OffsetDateTime occurredAt) {
        this.id = UUID.randomUUID();
        this.actionCode = QUERY_ACTION;
        this.entityType = BENEFICIARY_ENTITY;
        this.entityId = cpf;
        this.affectedCpf = cpf;
        this.description = "Consulta de cadastro de beneficiario - CONSBENF";
        this.moduleCode = "CONSBENF";
        this.occurredAt = occurredAt;
    }

    /**
     * Cria o registro de uma consulta de cadastro concluída com sucesso.
     *
     * @param cpf CPF do beneficiário consultado
     * @param occurredAt instante da consulta
     * @return registro pronto para persistência
     */
    static AuditTrail beneficiaryQuery(String cpf, OffsetDateTime occurredAt) {
        return new AuditTrail(cpf, occurredAt);
    }

    String actionCode() {
        return actionCode;
    }

    String entityType() {
        return entityType;
    }

    String affectedCpf() {
        return affectedCpf;
    }

    OffsetDateTime occurredAt() {
        return occurredAt;
    }
}
