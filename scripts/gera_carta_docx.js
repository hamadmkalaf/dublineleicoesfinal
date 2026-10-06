// Gera docs/cartas/modelo_carta_empregador.docx.
// Se docs/cartas/brasao.png existir, ele entra no timbre; senão fica o espaço reservado.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, BorderStyle } = require('docx');

const dir = path.join(__dirname, '..', 'docs', 'cartas');
const brasaoPath = path.join(dir, 'brasao.png');
const FONT = 'Calibri';
const run = (text, o = {}) => new TextRun({ text, font: FONT, size: 22, ...o });
const p = (children, o = {}) => new Paragraph({ spacing: { after: 160, line: 276 }, ...o, children: [].concat(children) });
const center = (text, o = {}) => p(run(text, o), { alignment: AlignmentType.CENTER, spacing: { after: 0 } });

const head = [];
if (fs.existsSync(brasaoPath)) {
  head.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new ImageRun({ type: 'png', data: fs.readFileSync(brasaoPath), transformation: { width: 80, height: 80 } })] }));
} else {
  head.push(center('[ BRASÃO DAS ARMAS DA REPÚBLICA — inserir docs/cartas/brasao.png e rodar o gerador ]', { size: 16, color: '999999' }));
}
head.push(center('REPÚBLICA FEDERATIVA DO BRASIL', { bold: true, size: 24 }));
head.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '444444', space: 6 } },
  children: [run('Eleições Presidenciais 2026 – Irlanda', { size: 20 })] }));

const body = [
  p(run('{{data_carta}}'), { alignment: AlignmentType.RIGHT }),
  p([run('{{nome_destinatario}}')], { spacing: { after: 0 } }),
  p([run('{{empresa}}')], { spacing: { after: 0 } }),
  p([run('{{endereco_empresa}}')], { spacing: { after: 240 } }),
  p(run('Re: Voluntary service by {{nome_voluntario}} at the 2026 Brazilian Presidential Elections, Dublin', { bold: true })),
  p(run('Dear {{nome_destinatario}},')),
  p(run('I am writing as the administrator of the 2026 Brazilian Presidential Elections in Ireland, to let you know that your employee, {{nome_voluntario}}, took part in the organisation of the first round of voting held in Dublin on Sunday, 4 October 2026.')),
  p(run('On that day, between 06:30 and 18:00, {{nome_voluntario}} served as a polling station worker. This was strictly voluntary work: it was unpaid, and it was carried out on {{pronome_poss}} own time, on a Sunday, in support of an election in which the Brazilian community in Ireland exercises its right to vote. We are very grateful for {{pronome_poss}} commitment.')),
  p(run('{{nome_voluntario}} was registered with the Brazilian Electoral Court (TRE) as part of the polling station team. Under Brazilian electoral law (Law No. 9,504/1997, Article 98), citizens who serve at polling stations, or who are called upon to assist them, are entitled to two days of leave, with no loss of pay, for each day worked. We understand that Brazilian law creates no obligation for employers in Ireland, and we do not suggest otherwise. We would, however, be grateful if you could consider, as a courtesy, granting {{nome_voluntario}} additional time off in recognition of the service {{pronome_poss}} performed.')),
  p(run('Should you require any confirmation of the dates and hours described above, please do not hesitate to contact us at {{contato}}.')),
  p(run('Thank you for your time and consideration.')),
  p(run('Yours sincerely,'), { spacing: { after: 720 } }),
  p(run('Eduardo de Mattos Hosannah', { bold: true }), { spacing: { after: 0 } }),
  p(run('Administrator, 2026 Brazilian Presidential Elections in Ireland'), { spacing: { after: 0 } }),
  p(run('{{contato}}')),
];

const doc = new Document({
  creator: 'Eleições 2026 – Posto de Dublin',
  title: 'Modelo de carta aos empregadores',
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1417, right: 1417 } } },
    children: [...head, ...body] }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(path.join(dir, 'modelo_carta_empregador.docx'), b); console.log('ok'); });
