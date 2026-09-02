import { Component, Input } from '@angular/core';
import { LordGuide, UnitGuide } from '../../models/guide.model';

@Component({
  selector: 'app-guide-lord',
  templateUrl: './guide-lord.component.html',
  styleUrl: './guide-lord.component.scss',
})
export class GuideLordComponent {
  @Input({ required: true }) lord!: LordGuide;
  @Input({ required: true }) accent = '#aaa';
  @Input({ required: true }) soft = '#181818';
  @Input({ required: true }) border = '#333';

  imageFailed = false;

  onImageError(): void {
    this.imageFailed = true;
  }

  trackUnit(_: number, unit: UnitGuide): string {
    return unit.id;
  }
}
