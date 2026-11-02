# Verificação do baseline versionado

Executada em 1 de novembro de 2026, durante a sincronização com o GitHub:

```bash
python3 scripts/check_branding.py --remote
```

Resultado: código de saída 0. Passaram hash SHA-256 local, assinatura PNG, dimensões 1774 × 887, canal RGBA, HTTP 200 do login, presença de nome/assinatura/cor no HTML, hash exato dos endpoints públicos logo e logoheader.

`git diff --check`: sem erros de whitespace.

Os arquivos destinados ao commit foram revisados por lista explícita. Nenhum config.php, .env, dump, credencial, backup privado ou captura de dados de usuários está incluído.

Esta validação só consulta o ambiente. Não executa deploy, upgrade, restart, upload de arquivos de usuários ou criação de compartilhamentos. Não certifica sincronização, recuperação de backup, visualização de PDFs nem compatibilidade com versões futuras.
