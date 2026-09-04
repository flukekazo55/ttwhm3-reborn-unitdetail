import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { GuideSharedModule } from '../../shared/modules/guide-shared/guide-shared.module';
import { CathayEffects } from '../../shared/stores/cathay/cathay.effect';
import { CATHAY_FEATURE_KEY, cathayReducer } from '../../shared/stores/cathay/cathay.reducer';
import { CathayComponent } from './cathay.component';

const routes: Routes = [
  { path: '', component: CathayComponent },
  { path: ':lordId', component: CathayComponent },
];

@NgModule({
  declarations: [CathayComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    StoreModule.forFeature(CATHAY_FEATURE_KEY, cathayReducer),
    EffectsModule.forFeature([CathayEffects]),
    ProgressSpinnerModule,
    GuideSharedModule,
  ],
})
export class CathayModule {}
