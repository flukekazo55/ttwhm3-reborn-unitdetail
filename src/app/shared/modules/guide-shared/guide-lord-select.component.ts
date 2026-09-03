import { Component, Input } from '@angular/core';
import { FactionGuide, LordGuide } from '../../models/guide.model';

@Component({
  selector: 'app-guide-lord-select',
  templateUrl: './guide-lord-select.component.html',
  styleUrl: './guide-lord-select.component.scss',
})
export class GuideLordSelectComponent {
  @Input({ required: true }) faction!: FactionGuide;

  failedPortraits = new Set<string>();

  onPortraitError(id: string): void {
    this.failedPortraits.add(id);
  }

  getCoreUnitNames(lord: LordGuide): string {
    return lord.coreUnits.slice(0, 3).map((unit) => unit.name).join(', ');
  }

  trackLord(_: number, lord: LordGuide): string {
    return lord.id;
  }
}
