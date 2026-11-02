# Estado observado em 1 de novembro de 2026

Instalação existente: Nextcloud 35.0.2 (versão interna 35.0.2.2), em Docker Compose. Este repositório não é a fonte do Compose de produção.

| Componente observado | Imagem |
|---|---|
| Aplicação e cron | nextcloud:35-fpm |
| Servidor web | nginx:1.28-alpine |
| Cache | redis:7.4-alpine |

Caminho observado do Compose: `/opt/aggilli-drive/deploy/docker-compose.yml`. Contêiner da aplicação: `aggilli-drive-app-1`. Volumes persistentes em `/srv/nextcloud/{html,config,data,custom_apps,themes}`. Confirmar esses valores na instalação alvo antes de executar comandos. Não copiar config.php ou .env para o Git.

## Antes do branding

Nome Aggilli Cloud, assinatura “Seus arquivos, com inteligência”, primary_color #2D8510, background_color #F5F8F4, disable-user-theming 1. Logos anteriores: PNG 800 × 181 no login e PNG 256 × 256 no cabeçalho.

## Após o branding

Nome, assinatura, cor, logo e logoheader conferidos. URL institucional, fundo, favicon e preferências existentes não foram alterados.

Verificações realizadas no deploy: login HTTP 200; nome/assinatura/cor no HTML; hashes exatos das duas imagens públicas; nova logo visível no login; occ status installed=true, maintenance=false, needsDbUpgrade=false; quatro contêineres ativos sem reinício.

A página autenticada de arquivos foi conferida após a alteração dos três campos de texto/cor. Após a troca da logo, o asset do cabeçalho foi confirmado por hash, mas a renderização do cabeçalho autenticado ficou pendente. Não foram testados novo login, upload/download, criação de links, sincronização, mobile, recuperação de backup ou persistência após restart.

Erro de console observado em files_pdfviewer-main.js: TypeError ao acessar registerHandler. Causa e origem temporal não estabelecidas; aplicativo não modificado. Não atribuir a falha ao branding sem investigar.

Backups privados das duas logos anteriores permanecem no servidor em `/opt/aggilli-drive/branding-backups/2026-11-01-logo/`. Eles não foram publicados neste repositório.
