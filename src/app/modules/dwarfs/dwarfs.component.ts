import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { map, Observable } from 'rxjs';
import { FactionGuideViewModel } from '../../shared/models/guide.model';
import { loadDwarfs } from '../../shared/stores/dwarfs/dwarfs.action';
import { selectDwarfsVm } from '../../shared/stores/dwarfs/dwarfs.selector';

@Component({
  selector: 'app-dwarfs',
  templateUrl: './dwarfs.component.html',
  styleUrl: './dwarfs.component.scss',
  host: { class: 'faction-dark' },
})
export class DwarfsComponent implements OnInit {
  private store = inject(Store);
  private route = inject(ActivatedRoute);

  readonly pageTitle = 'DWARFS';
  vm$: Observable<FactionGuideViewModel> = this.store.select(selectDwarfsVm);
  lordId$: Observable<string | null> = this.route.paramMap.pipe(map((p) => p.get('lordId')));

  ngOnInit(): void {
    this.store.dispatch(loadDwarfs());
  }
}
