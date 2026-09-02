import { Component, inject, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
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

  readonly pageTitle = 'KISLEV';
  vm$: Observable<FactionGuideViewModel> = this.store.select(selectKislevVm);

  ngOnInit(): void {
    this.store.dispatch(loadKislev());
  }
}
