"""
Validadores customizados para o projeto ihelp.
Inclui validação de CPF e CNPJ.
"""
import re

from django.core.exceptions import ValidationError


def validate_cpf(cpf):
    """
    Valida um CPF brasileiro.
    Formato esperado: 11 dígitos ou XXX.XXX.XXX-XX
    """
    cpf = re.sub(r'\D', '', cpf)
    
    if len(cpf) != 11:
        raise ValidationError("CPF deve conter 11 dígitos.")
    
    # Verifica se todos os dígitos são iguais (CPFs inválidos)
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido (dígitos repetidos).")
    
    # Calcula primeiro dígito verificador
    sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = 11 - (sum_digits % 11)
    first_digit = 0 if first_digit >= 10 else first_digit
    
    if int(cpf[9]) != first_digit:
        raise ValidationError("CPF inválido (primeiro dígito verificador incorreto).")
    
    # Calcula segundo dígito verificador
    sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = 11 - (sum_digits % 11)
    second_digit = 0 if second_digit >= 10 else second_digit
    
    if int(cpf[10]) != second_digit:
        raise ValidationError("CPF inválido (segundo dígito verificador incorreto).")


def validate_cnpj(cnpj):
    """
    Valida um CNPJ brasileiro.
    Formato esperado: 14 dígitos ou XX.XXX.XXX/XXXX-XX
    """
    cnpj = re.sub(r'\D', '', cnpj)
    
    if len(cnpj) != 14:
        raise ValidationError("CNPJ deve conter 14 dígitos.")
    
    # Verifica se todos os dígitos são iguais (CNPJs inválidos)
    if cnpj == cnpj[0] * 14:
        raise ValidationError("CNPJ inválido (dígitos repetidos).")
    
    # Calcula primeiro dígito verificador
    multipliers = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * multipliers[i] for i in range(12))
    first_digit = 11 - (sum_digits % 11)
    first_digit = 0 if first_digit >= 10 else first_digit
    
    if int(cnpj[12]) != first_digit:
        raise ValidationError("CNPJ inválido (primeiro dígito verificador incorreto).")
    
    # Calcula segundo dígito verificador
    multipliers = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3]
    sum_digits = sum(int(cnpj[i]) * multipliers[i] for i in range(12))
    second_digit = 11 - (sum_digits % 11)
    second_digit = 0 if second_digit >= 10 else second_digit
    
    if int(cnpj[13]) != second_digit:
        raise ValidationError("CNPJ inválido (segundo dígito verificador incorreto).")


def validate_phone_number(phone):
    """
    Valida um número de telefone brasileiro.
    Aceita formatos: (XX)XXXXX-XXXX, (XX)XXXX-XXXX, XXXXXXXXXX, XXXXXXXXXXX
    """
    phone = re.sub(r'\D', '', phone)
    
    if len(phone) not in [10, 11]:
        raise ValidationError("Telefone deve ter 10 ou 11 dígitos.")
    
    # Verifica se começa com dígito válido
    if phone[0] not in '123456789':
        raise ValidationError("Número de telefone inválido.")
