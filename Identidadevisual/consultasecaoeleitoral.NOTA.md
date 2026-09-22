# consultasecaoeleitoral.svg — o QR recebido em 22/09

Arquivo entregue pelo Posto em 22/09/2026 (subiu ao repositório de origem
`hamadmkalaf/eleicoes2026`, commit `8295bcd`, porque o upload direto falhou).
É um QR de 1024 × 1024 px com moldura "Scan me!" e a fonte Inter embutida em
base64 (80 KB).

**Decodificado com OpenCV: `https://link.getqr.com/XwlEKkK`.** Não é a URL do
TSE: é um link dinâmico da getqr.com, um encurtador de terceiro, cujo destino
pode ser trocado sem que o Posto saiba e cujo serviço pode expirar antes de
04/10. Daqui não foi possível seguir o redirecionamento (o proxy bloqueia o
host).

**Por isso ele não entra na peça.** Decisão do Posto de 22/09: a P0-Consulta
leva um QR **estático**, gerado por `scripts/qr_tse.py` (nível de correção H)
direto para a consulta de seção por nome no site do TSE. A URL é a constante
`URL` do script; se o Posto preferir outra página do TSE, muda ali e regrava.

O arquivo fica guardado aqui como referência do que foi recebido.
