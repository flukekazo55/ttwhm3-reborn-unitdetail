import { Component } from '@angular/core';

interface FactionChoice {
  id: string;
  name: string;
  subtitle: string;
  blurb: string;
  emoji: string;
  accent: string;
  soft: string;
  art: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  readonly factions: FactionChoice[] = [
    {
      id: 'khorne',
      name: 'Khorne',
      subtitle: 'Blood for the Blood God',
      blurb: 'สายบุกประชิด เน้น momentum ปิดไฟต์ไว ๆ มันส์สุด ๆ',
      emoji: '🔥',
      accent: '#ef6a48',
      soft: '#ffe7df',
      art: 'assets/lords/khorne/chibi/skarbrand-lord.svg',
    },
    {
      id: 'kislev',
      name: 'Kislev',
      subtitle: 'The Motherland Endures',
      blurb: 'กองทัพ hybrid ยิง–รับ–เวท–ม้า–สัตว์ ยืดหยุ่นสุด',
      emoji: '❄️',
      accent: '#3f9be0',
      soft: '#e4f1fc',
      art: 'assets/lords/kislev/chibi/katarin-lord.svg',
    },
    {
      id: 'cathay',
      name: 'Grand Cathay',
      subtitle: 'The Celestial Empire Endures',
      blurb: 'สายตั้งรับ ยืนแนวค้ำหน้า แล้วให้ปืน เวท และ Harmony ทำงาน',
      emoji: '🐉',
      accent: '#2f9e78',
      soft: '#e3f5ed',
      art: 'assets/lords/cathay/chibi/miao-ying-lord.svg',
    },
    {
      id: 'dwarfs',
      name: 'Dwarfs',
      subtitle: 'Grudges Are Never Forgotten',
      blurb: 'ไม่มีเวทเลย แลกด้วยเกราะหนา ปืนแม่น และไลน์ที่ไม่แตก',
      emoji: '🔨',
      accent: '#b8762b',
      soft: '#f7ecd9',
      art: 'assets/lords/dwarfs/chibi/thorgrim-lord.svg',
    },
  ];

  failedArt = new Set<string>();

  onArtError(id: string): void {
    this.failedArt.add(id);
  }

  trackFaction(_: number, faction: FactionChoice): string {
    return faction.id;
  }
}
