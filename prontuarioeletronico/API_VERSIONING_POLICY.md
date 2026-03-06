# Política de Versionamento de APIs

## Objetivo

Padronizar evolução de contratos HTTP dos serviços (`auth-service`, `patient-service`, `gateway-service`) reduzindo risco de quebra para consumidores.

## Princípios

1. Toda API pública deve ser versionada no path (`/api/v1/...`).
2. Mudanças aditivas (novos endpoints/campos opcionais) são permitidas na mesma major.
3. Breaking changes exigem nova major (`v2`) e plano de migração.
4. Remoção de endpoint na mesma major é proibida.
5. CI deve bloquear regressões de contrato na major atual.

## Definição de Breaking Change (baseline atual)

No escopo desta política inicial, considera-se breaking change:

- remoção de endpoint existente (`path + método`) na major ativa.

## Processo de Evolução

1. Alterar API com compatibilidade retroativa (preferencialmente aditiva).
2. Executar check de breaking changes localmente.
3. Em caso de nova major planejada:
   - documentar migração;
   - atualizar baseline e versão da API.

## Governança

- Baseline de compatibilidade: `contracts/api_compatibility_baseline.json`
- Validador de compatibilidade: `scripts/check_api_breaking_changes.py`
- Execução automática no CI: job `api-compatibility-check`
