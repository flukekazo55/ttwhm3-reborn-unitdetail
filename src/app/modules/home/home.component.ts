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
      art: 'assets/lords/khorne/chibi/skarbrand-lord.png',
    },
    {
      id: 'kislev',
      name: 'Kislev',
      subtitle: 'The Motherland Endures',
      blurb: 'กองทัพ hybrid ยิง–รับ–เวท–ม้า–สัตว์ ยืดหยุ่นสุด',
      emoji: '❄️',
      accent: '#3f9be0',
      soft: '#e4f1fc',
      art: 'assets/lords/kislev/chibi/katarin-lord.png',
    },
  ];

  trackFaction(_: number, faction: FactionChoice): string {
    return faction.id;
  }
}
