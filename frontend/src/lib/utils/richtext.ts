export interface Segment {
  text: string;
  bold: boolean;
  italic: boolean;
}

export type Leaf =
  | { type: 'h'; segments: Segment[] }
  | { type: 'p'; lines: Segment[][] }
  | { type: 'ul' | 'ol'; items: Segment[][] };

export type Block = Leaf | { type: 'answers'; title: Segment[]; blocks: Leaf[] };

const ANSWERS = /^(answers?|answer key|solutions?|réponses?|corrigés?|respuestas?)\b/i;
const PIECES = /(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)/g;

function inline(text: string): Segment[] {
  return text
    .split(PIECES)
    .filter(Boolean)
    .map((part) => {
      if (part.length > 4 && part.startsWith('**') && part.endsWith('**')) return { text: part.slice(2, -2), bold: true, italic: false };
      if (part.length > 2 && part.startsWith('*') && part.endsWith('*')) return { text: part.slice(1, -1), bold: false, italic: true };
      return { text: part, bold: false, italic: false };
    });
}

const plain = (segments: Segment[]) => segments.map((segment) => segment.text).join('').trim();

function leaves(source: string): Leaf[] {
  const out: Leaf[] = [];
  let paragraph: Segment[][] = [];
  const flush = () => {
    if (paragraph.length) out.push({ type: 'p', lines: paragraph });
    paragraph = [];
  };

  for (const raw of source.split('\n')) {
    const line = raw.trim();
    if (!line) {
      flush();
      continue;
    }
    const heading = line.match(/^#{1,6}\s*(.+)/) ?? line.match(/^\*\*([^*]+)\*\*:?$/);
    if (heading) {
      flush();
      out.push({ type: 'h', segments: inline(heading[1].replace(/[:\s]+$/, '')) });
      continue;
    }
    const bullet = line.match(/^[-•*]\s+(.*)/);
    const numbered = line.match(/^\d+[.)]\s+(.*)/);
    const kind = bullet ? 'ul' : numbered ? 'ol' : null;
    if (kind) {
      flush();
      const item = inline((bullet ?? numbered)![1]);
      const last = out[out.length - 1];
      if (last && (last.type === 'ul' || last.type === 'ol') && last.type === kind) last.items.push(item);
      else out.push({ type: kind, items: [item] });
      continue;
    }
    paragraph.push(inline(line));
  }
  flush();
  return out;
}

export function parseRichText(source: string): Block[] {
  const flat = leaves(source);
  const out: Block[] = [];
  for (let i = 0; i < flat.length; i++) {
    const block = flat[i];
    if (block.type === 'h' && ANSWERS.test(plain(block.segments))) {
      const inner: Leaf[] = [];
      while (i + 1 < flat.length && flat[i + 1].type !== 'h') inner.push(flat[++i]);
      out.push({ type: 'answers', title: block.segments, blocks: inner });
    } else out.push(block);
  }
  return out;
}