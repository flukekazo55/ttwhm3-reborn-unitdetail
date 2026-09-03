import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { map, Observable } from 'rxjs';
import { FactionGuideViewModel } from '../../shared/models/guide.model';
import { loadKislev } from '../../shared/stores/kislev/kislev.action';
import { selectKislevVm } from '../../shared/stores/kislev/kislev.selector';

@Component({
  selector: 'app-kislev',
  templateUrl: './kislev.component.html',
  styleUrl: './kislev.component.scss',
})
export class KislevComponent implements OnInit {
  private store = inject(Store);
  private route = inject(ActivatedRoute);

  readonly pageTitle = 'KISLEV';
  vm$: Observable<FactionGuideViewModel> = this.store.select(selectKislevVm);
  lordId$: Observable<string | null> = this.route.paramMap.pipe(map((p) => p.get('lordId')));

  ngOnInit(): void {
    this.store.dispatch(loadKislev());
  }
}
