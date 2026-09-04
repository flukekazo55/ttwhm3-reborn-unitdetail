import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { map, Observable } from 'rxjs';
import { FactionGuideViewModel } from '../../shared/models/guide.model';
import { loadCathay } from '../../shared/stores/cathay/cathay.action';
import { selectCathayVm } from '../../shared/stores/cathay/cathay.selector';

@Component({
  selector: 'app-cathay',
  templateUrl: './cathay.component.html',
  styleUrl: './cathay.component.scss',
})
export class CathayComponent implements OnInit {
  private store = inject(Store);
  private route = inject(ActivatedRoute);

  readonly pageTitle = 'GRAND CATHAY';
  vm$: Observable<FactionGuideViewModel> = this.store.select(selectCathayVm);
  lordId$: Observable<string | null> = this.route.paramMap.pipe(map((p) => p.get('lordId')));

  ngOnInit(): void {
    this.store.dispatch(loadCathay());
  }
}
