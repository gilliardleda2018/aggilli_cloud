# Aplicação e reversão do branding

Não há deploy automático. A sincronização deste repositório não altera a instalação. Os comandos abaixo são um procedimento manual para um operador autorizado na máquina alvo; não devem ser executados como parte de uma atualização sem revisão.

Referência oficial: https://docs.nextcloud.com/server/stable/admin_manual/occ_system.html#theming-config

## Preparar

1. Confirmar ambiente, contêiner e versão. Comprovar backup operacional recuperável antes de atualizar a aplicação. Uma cópia de logo não é backup de banco ou dados.
2. Clonar o repositório em diretório separado da instalação, selecionar o commit aprovado e executar `python3 scripts/check_branding.py`.
3. Consultar `docker exec --user www-data CONTAINER php occ help theming:config`, `status --output=json` e `theming:config`. Confirmar suporte às cinco chaves. Não usar comandos de upgrade, repair ou reset para aplicar branding.
4. Registrar os valores atuais e guardar logos atuais e respectivos hashes num diretório restrito do servidor. Usar os endpoints públicos observados `/apps/theming/image/logo` e `/apps/theming/image/logoheader` para as cópias; verificar HTTP e que os arquivos são PNGs válidos. Se qualquer backup falhar, parar antes da escrita.
5. Confirmar o ativo e o hash aprovados no manifesto. A fonte desta implantação é PNG, não SVG.

## Aplicar somente após autorização

Executar na raiz do checkout aprovado, **na máquina que executa o Docker**, com acesso ao daemon. Os valores abaixo são os auditados; adaptar CONTAINER apenas após inspeção.

```bash
CONTAINER=aggilli-drive-app-1
docker cp assets/brand/nuvem-aggilli-transparente.png "$CONTAINER":/tmp/nuvem-aggilli-brand.png
docker exec --user www-data "$CONTAINER" php occ theming:config name 'Nuvem Aggilli'
docker exec --user www-data "$CONTAINER" php occ theming:config slogan 'Seus dados, seu controle, em qualquer lugar.'
docker exec --user www-data "$CONTAINER" php occ theming:config primary_color '#0866F5'
docker exec --user www-data "$CONTAINER" php occ theming:config logo /tmp/nuvem-aggilli-brand.png
docker exec --user www-data "$CONTAINER" php occ theming:config logoheader /tmp/nuvem-aggilli-brand.png
```

Executar e conferir um comando por vez. Interromper em qualquer erro, registrar quais campos foram aplicados e avaliar reversão. As cinco escritas não são uma transação atômica. O Nextcloud importa o asset para seu armazenamento gerenciado de theming; o arquivo em /tmp serve apenas como entrada, não como dependência do logo em execução.

Não reiniciar serviços, editar core, modificar autenticação, alterar permissões de volumes ou executar `docker compose down -v` para aplicar a identidade. Não substituir o Compose existente por um arquivo inventado a partir deste repositório.

## Validar

Consultar novamente theming:config e status. Executar `python3 scripts/check_branding.py --remote`. Conferir visualmente login e cabeçalho em sessão autenticada, desktop/mobile e foco por teclado. Verificar console. Testar login/logout, upload/download e compartilhamento em homologação com arquivos de teste identificados. Informar separadamente verificações executadas e pendentes.

## Rollback registrado desta implantação

Antes da alteração de imagem foram guardados no servidor:

- `/opt/aggilli-drive/branding-backups/2026-11-01-logo/logo-before.png`
- `/opt/aggilli-drive/branding-backups/2026-11-01-logo/logoheader-before.png`

Para reverter **somente as imagens**, um operador autorizado pode executar, na mesma instância:

```bash
sudo docker cp /opt/aggilli-drive/branding-backups/2026-11-01-logo/logo-before.png aggilli-drive-app-1:/tmp/aggilli-logo-before.png
sudo docker cp /opt/aggilli-drive/branding-backups/2026-11-01-logo/logoheader-before.png aggilli-drive-app-1:/tmp/aggilli-logoheader-before.png
sudo docker exec --user www-data aggilli-drive-app-1 php occ theming:config logo /tmp/aggilli-logo-before.png
sudo docker exec --user www-data aggilli-drive-app-1 php occ theming:config logoheader /tmp/aggilli-logoheader-before.png
```

Para reverter também os três campos iniciais, restaurar `name='Aggilli Cloud'`, `slogan='Seus arquivos, com inteligência'` e `primary_color='#2D8510'` pela mesma interface. Esses valores são o baseline de 1 de novembro de 2026; em uma implantação posterior usar o backup daquela implantação.

Rollback documentado, não testado nesta sessão. A verificação do manifesto atual deve divergir após uma reversão intencional; não reimplantar automaticamente. Não restaurar banco ou volume inteiro para desfazer uma mudança de logo.
