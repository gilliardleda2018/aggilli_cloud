# Atualização do Nextcloud sem perder o branding

O repositório permite recuperar os assets e os valores aprovados. Ele não substitui a instalação nem garante compatibilidade com qualquer versão futura.

## Antes

1. Identificar a versão atual, a versão alvo e os passos de upgrade oficialmente suportados. Não atualizar diretamente para uma major arbitrária. Ler documentação e notas da versão alvo.
2. Identificar o repositório real do Compose/infraestrutura: não está contido aqui. Capturar versões e referências/digests das imagens realmente em execução. As tags observadas são referências históricas, não pins imutáveis.
3. Confirmar backup consistente e recuperável de banco, dados, configurações e armazenamento de appdata/theming, incluindo eventual object storage. Não presumir que copiar somente `/srv/nextcloud` cobre tudo. Preparar rollback operacional específico para a atualização; downgrade do Nextcloud não deve ser presumido seguro.
4. Executar o verificador local e `--remote`; registrar o commit do branding e o resultado como baseline. Documentar falhas já existentes, inclusive o erro observado no PDF viewer.
5. Ensaiar a atualização numa homologação isolada com o mesmo modelo de persistência. Não conectar cron, e-mail, sync ou compartilhamentos desse ambiente aos dados de produção sem planejamento.

## Depois, em homologação

1. Confirmar status, apps compatíveis e ausência de upgrade de banco pendente.
2. Conferir nome, assinatura, cor, logo e cabeçalho. Executar o verificador contra a URL de homologação. Um hash diferente pode ser conversão da versão nova: investigar e revisar o manifesto, sem aceitar automaticamente.
3. Verificar login/logout, upload/download, visualização de arquivos, compartilhamento, sincronização, responsividade, acessibilidade e console.
4. Reiniciar somente a homologação para testar persistência e repetir as verificações de branding.
5. Abrir PR com mudanças necessárias e evidências; obter aprovação para produção. Este repositório não inicia atualizações de produção ao receber commits.

## Produção

Aplicar apenas o plano aprovado, com backup e janela definidos. Repetir verificações. Se o branding persistiu, não reaplicá-lo. Se houver divergência, diagnosticar a causa antes de usar o procedimento de aplicação. Não modificar core nem instalar extensões de CSS como correção automática.

Registrar versão final, commit de referência, testes realmente realizados e eventuais pendências no CHANGELOG e no registro operacional privado. Não publicar credenciais, tokens, config.php, .env, dumps, dados de usuários ou capturas com documentos pessoais.
