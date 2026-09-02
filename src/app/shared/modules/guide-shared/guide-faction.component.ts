import { Component, Input, OnChanges } from '@angular/core';
import { FactionGuide, LordGuide } from '../../models/guide.model';

@Component({
  selector: 'app-guide-faction',
  templateUrl: './guide-faction.component.html',
  styleUrl: './guide-faction.component.scss',
})
export class GuideFactionComponent implements OnChanges {
  @Input({ required: true }) faction!: FactionGuide;

  selectedLordId = '';

  ngOnChanges(): void {
    const stillExists = this.faction?.lords.some((l) => l.id === this.selectedLordId);
    if (!stillExists) {
      this.selectedLordId = this.faction?.lords[0]?.id ?? '';
    }
  }

  get selectedLord(): LordGuide | undefined {
    return this.faction.lords.find((l) => l.id === this.selectedLordId);
  }

  selectLord(id: string): void {
    this.selectedLordId = id;
  }

  trackLord(_: number, lord: LordGuide): string {
    return lord.id;
  }

  getCoreUnitNames(lord: LordGuide): string {
    return lord.coreUnits.slice(0, 3).map((unit) => unit.name).join(', ');
  }
}
