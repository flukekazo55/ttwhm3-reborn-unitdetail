import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { GuideSharedModule } from '../../shared/modules/guide-shared/guide-shared.module';
import { KislevEffects } from '../../shared/stores/kislev/kislev.effect';
import { KISLEV_FEATURE_KEY, kislevReducer } from '../../shared/stores/kislev/kislev.reducer';
import { KislevComponent } from './kislev.component';

const routes: Routes = [
  { path: '', component: KislevComponent },
  { path: ':lordId', component: KislevComponent },
];

@NgModule({
  declarations: [KislevComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    StoreModule.forFeature(KISLEV_FEATURE_KEY, kislevReducer),
    EffectsModule.forFeature([KislevEffects]),
    ProgressSpinnerModule,
    GuideSharedModule,
  ],
})
export class KislevModule {}
