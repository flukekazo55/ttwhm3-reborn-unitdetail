import { Component } from '@angular/core';

interface FactionChoice {
  id: string;
  name: string;
  subtitle: string;
  blurb: string;
  emblem: string;
  accent: string;
  soft: string;
  art: string;
  dark?: boolean;
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
      emblem: 'assets/emblems/khorne.svg',
      accent: '#ef6a48',
      soft: '#ffe7df',
      art: 'assets/shields/khorne.svg',
    },
    {
      id: 'kislev',
      name: 'Kislev',
      subtitle: 'The Motherland Endures',
      blurb: 'กองทัพ hybrid ยิง–รับ–เวท–ม้า–สัตว์ ยืดหยุ่นสุด',
      emblem: 'assets/emblems/kislev.svg',
      accent: '#3f9be0',
      soft: '#e4f1fc',
      art: 'assets/shields/kislev.svg',
    },
    {
      id: 'cathay',
      name: 'Grand Cathay',
      subtitle: 'The Celestial Empire Endures',
      blurb: 'สายตั้งรับ ยืนแนวค้ำหน้า แล้วให้ปืน เวท และ Harmony ทำงาน',
      emblem: 'assets/emblems/cathay.svg',
      accent: '#2f9e78',
      soft: '#e3f5ed',
      art: 'assets/shields/cathay.svg',
    },
    {
      id: 'dwarfs',
      name: 'Dwarfs',
      subtitle: 'Grudges Are Never Forgotten',
      blurb: 'ไม่มีเวทเลย แลกด้วยเกราะหนา ปืนแม่น และไลน์ที่ไม่แตก',
      emblem: 'assets/emblems/dwarfs.svg',
      accent: '#d99a45',
      soft: '#241d16',
      art: 'assets/shields/dwarfs.svg',
      dark: true,
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
