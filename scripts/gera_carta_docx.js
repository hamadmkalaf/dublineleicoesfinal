// Sem argumentos: gera docs/cartas/modelo_carta_empregador.docx (modelo com campos {{...}}).
// Com dados:  node scripts/gera_carta_docx.js dados.json pasta_saida [--data "7 October 2026"] [--contato "..."]
// dados.json vem de scripts/xlsx_para_json.py. Gera um .docx por pessoa, nomeado com o nome dela.
// Se docs/cartas/brasao.png existir, ele entra no timbre; senão fica o espaço reservado.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, BorderStyle } = require('docx');

const dir = path.join(__dirname, '..', 'docs', 'cartas');
const brasaoPath = path.join(dir, 'brasao.png');
const FONT = 'Calibri';
const baseRun = (text, o = {}) => new TextRun({ text, font: FONT, size: 22, ...o });
const run = baseRun;
const p = (children, o = {}) => new Paragraph({ spacing: { after: 160, line: 276 }, ...o, children: [].concat(children) });
const center = (text, o = {}) => p(run(text, o), { alignment: AlignmentType.CENTER, spacing: { after: 0 } });

const head = [];
if (fs.existsSync(brasaoPath)) {
  head.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new ImageRun({ type: 'png', data: fs.readFileSync(brasaoPath), transformation: { width: 84, height: 84 } })] }));
} else {
  head.push(center('[ BRASÃO DAS ARMAS DA REPÚBLICA — inserir docs/cartas/brasao.png e rodar o gerador ]', { size: 16, color: '999999' }));
}
head.push(center('REPÚBLICA FEDERATIVA DO BRASIL', { bold: true, size: 24 }));
head.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '444444', space: 6 } },
  children: [run('Embaixada do Brasil na Irlanda', { size: 20 })] }));

const buildBody = (f) => {
  const T = (x) => x
    .replace(/\{\{nome_voluntario\}\}/g, f.nome || '{{nome_voluntario}}')
    .replace(/\{\{pronome_poss\}\}/g, f.pronome || '{{pronome_poss}}')
    .replace(/\{\{data_carta\}\}/g, f.data || '{{data_carta}}')
    .replace(/\{\{contato\}\}/g, f.contato || '{{contato}}')
    .replace(/\{\{nome_destinatario\}\}/g, f.empresas ? 'Sir or Madam' : '{{nome_destinatario}}');
  const run = (text, o) => baseRun(T(text), o);
  const addr = f.empresas ? ['Human Resources Department', ...f.empresas] : ['{{nome_destinatario}}', '{{empresa}}', '{{endereco_empresa}}'];
  return [
  p(run('{{data_carta}}'), { alignment: AlignmentType.RIGHT }),
  ...addr.map((l, i) => p([run(l)], { spacing: { after: i === addr.length - 1 ? 240 : 0 } })),
  p(run('Re: Voluntary service by {{nome_voluntario}} at the 2026 Brazilian Presidential Elections, Dublin', { bold: true })),
  p(run('Dear {{nome_destinatario}},')),
  p(run('I am writing as the administrator of the 2026 Brazilian Presidential Elections in Ireland, to let you know that your employee, {{nome_voluntario}}, took part in the organisation of the first round of voting held in Dublin on Sunday, 4 October 2026, for which we are extremely grateful.')),
  p(run('On that day, between 06:30 and 18:00, {{nome_voluntario}} served as a polling station worker. This was strictly voluntary work: it was unpaid, and it was carried out on {{pronome_poss}} own time, on a Sunday, in support of an election in which the Brazilian community in Ireland exercises its right to vote. We would like to let you know that {{pronome_poss}} work was exceptionally useful and we are very grateful for {{pronome_poss}} commitment.')),
  p(run('Under Brazilian electoral law (Law No. 9,504/1997, Article 98), citizens who serve at polling stations, or who are called upon to assist them, are entitled to two days of leave, with no loss of pay, for each day worked. We understand that Brazilian law creates no obligation for employers in Ireland, and we do not suggest otherwise. We would, however, be grateful if you could consider, as a courtesy, granting {{nome_voluntario}} additional time off in recognition of {{pronome_poss}} service, or any other kind of reward you would consider appropriate.')),
  p(run('Should you require any confirmation of the dates and hours described above, please do not hesitate to contact us at {{contato}}')),
  p(run('Thank you for your time and consideration.')),
  p(run('Yours sincerely,'), { spacing: { after: 720 } }),
  p(run('Eduardo de Mattos Hosannah', { bold: true }), { spacing: { after: 0 } }),
  p(run('Administrator of the 2026 Brazilian Presidential Elections in Ireland')),
];
};

const makeDoc = (f) => new Document({
  creator: 'Embaixada do Brasil na Irlanda',
  title: 'Carta ao empregador',
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1417, right: 1417 } } },
    children: [...head, ...buildBody(f)] }],
});

const [dadosPath, outDir, ...rest] = process.argv.slice(2);
const opt = (k) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : undefined; };
(async () => {
  if (!dadosPath) {
    fs.writeFileSync(path.join(dir, 'modelo_carta_empregador.docx'), await Packer.toBuffer(makeDoc({})));
    return console.log('modelo ok');
  }
  fs.mkdirSync(outDir, { recursive: true });
  const data = opt('--data') || '6 October 2026';
  for (const v of JSON.parse(fs.readFileSync(dadosPath, 'utf8'))) {
    // uma_carta_por_empresa: cada empregador recebe a sua, sem ver os outros
    const lotes = v.uma_carta_por_empresa ? v.empresas.map((e) => ({ empresas: [e], arq: `${v.nome} - ${e}` })) : [{ empresas: v.empresas, arq: v.nome }];
    for (const l of lotes) {
      const buf = await Packer.toBuffer(makeDoc({ nome: v.nome, pronome: v.pronome_poss, empresas: l.empresas, data, contato: opt('--contato') || 'eleitoral.dublin@itamaraty.gov.br' }));
      fs.writeFileSync(path.join(outDir, `${l.arq}.docx`), buf);
    }
  }
  console.log('cartas ok');
})();
