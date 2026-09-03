import { Component, Input, OnChanges } from '@angular/core';
import { FactionGuide, LordGuide } from '../../models/guide.model';

@Component({
  selector: 'app-guide-lord-detail',
  templateUrl: './guide-lord-detail.component.html',
  styleUrl: './guide-lord-detail.component.scss',
})
export class GuideLordDetailComponent implements OnChanges {
  @Input({ required: true }) faction!: FactionGuide;
  @Input({ required: true }) lordId!: string;

  selectedLord?: LordGuide;

  ngOnChanges(): void {
    this.selectedLord =
      this.faction?.lords.find((l) => l.id === this.lordId) ?? this.faction?.lords[0];
  }

  trackLord(_: number, lord: LordGuide): string {
    return lord.id;
  }
}
