import { Component, Input } from '@angular/core';
import { UnitGuide, UnitStat } from '../../models/guide.model';

@Component({
  selector: 'app-guide-unit-card',
  templateUrl: './guide-unit-card.component.html',
  styleUrl: './guide-unit-card.component.scss',
})
export class GuideUnitCardComponent {
  @Input({ required: true }) unit!: UnitGuide;
  @Input({ required: true }) accent = '#aaa';

  imageFailed = false;

  onImageError(): void {
    this.imageFailed = true;
  }

  trackStat(_: number, stat: UnitStat): string {
    return stat.label;
  }

  trackTrait(_: number, trait: string): string {
    return trait;
  }
}
