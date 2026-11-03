export interface Segment {
  text: string;
  bold: boolean;
}
export type Block = { type: 'p'; segments: Segment[] } | { type: 'ul'; items: Segment[][] };

function inline(text: string): Segment[] {
  return text
    .split(/\*\*(.+?)\*\*/g)
    .map((part, index) => ({ text: part, bold: index % 2 === 1 }))
    .filter((segment) => segment.text);
}

export function parseRichText(source: string): Block[] {
  const blocks: Block[] = [];
  for (const raw of source.split('\n')) {
    const line = raw.trim();
    if (!line) continue;
    const item = line.match(/^[-•*]\s+(.*)/);
    if (item) {
      const last = blocks[blocks.length - 1];
      if (last?.type === 'ul') last.items.push(inline(item[1]));
      else blocks.push({ type: 'ul', items: [inline(item[1])] });
    } else {
      blocks.push({ type: 'p', segments: inline(line.replace(/^#+\s*/, '')) });
    }
  }
  return blocks;
}
