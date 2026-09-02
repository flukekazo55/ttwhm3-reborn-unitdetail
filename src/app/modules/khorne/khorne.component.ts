import { Component, inject, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { FactionGuideViewModel } from '../../shared/models/guide.model';
import { loadKhorne } from '../../shared/stores/khorne/khorne.action';
import { selectKhorneVm } from '../../shared/stores/khorne/khorne.selector';

@Component({
  selector: 'app-khorne',
  templateUrl: './khorne.component.html',
  styleUrl: './khorne.component.scss',
})
export class KhorneComponent implements OnInit {
  private store = inject(Store);

  readonly pageTitle = 'KHORNE';
  vm$: Observable<FactionGuideViewModel> = this.store.select(selectKhorneVm);

  ngOnInit(): void {
    this.store.dispatch(loadKhorne());
  }
}
