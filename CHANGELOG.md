# Changelog

## 2026-11-01 — baseline do branding em produção

- Nome alterado de Aggilli Cloud para Nuvem Aggilli.
- Assinatura alterada para “Seus dados, seu controle, em qualquer lugar.”.
- primary_color alterada de #2D8510 para #0866F5.
- Logo transparente sem quadriculado e sem ® aplicada a logo e logoheader pelo occ.
- Hash do asset transferido e das duas respostas públicas confirmado; backups anteriores mantidos no servidor.
- Login HTTP 200; status operacional conferido; contêineres sem restart.
- Asset e manifesto versionados, com verificador de integridade e runbooks de implantação, rollback e atualização.
- Sem alterações em armazenamento, autenticação, compartilhamentos ou infraestrutura. Sem deploy automático pelo GitHub.

### Limitações registradas

- Cabeçalho autenticado não inspecionado visualmente após a troca da imagem.
- Upload/download/sincronização e restauração de backup não testados nesta implantação.
- Erro JavaScript em files_pdfviewer registrado, sem causa estabelecida ou correção aplicada.
- Logo derivada de raster por edição de IA; pequenas irregularidades remanescentes informadas e aceitas para deploy.
- Favicon, fonte Plus Jakarta Sans e fundo institucional ainda não implantados.
