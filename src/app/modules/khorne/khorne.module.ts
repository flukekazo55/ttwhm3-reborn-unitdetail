import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { GuideSharedModule } from '../../shared/modules/guide-shared/guide-shared.module';
import { KhorneEffects } from '../../shared/stores/khorne/khorne.effect';
import { KHORNE_FEATURE_KEY, khorneReducer } from '../../shared/stores/khorne/khorne.reducer';
import { KhorneComponent } from './khorne.component';

const routes: Routes = [{ path: '', component: KhorneComponent }];

@NgModule({
  declarations: [KhorneComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    StoreModule.forFeature(KHORNE_FEATURE_KEY, khorneReducer),
    EffectsModule.forFeature([KhorneEffects]),
    ProgressSpinnerModule,
    GuideSharedModule,
  ],
})
export class KhorneModule {}
