import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { GuideSharedModule } from '../../shared/modules/guide-shared/guide-shared.module';
import { DwarfsEffects } from '../../shared/stores/dwarfs/dwarfs.effect';
import { DWARFS_FEATURE_KEY, dwarfsReducer } from '../../shared/stores/dwarfs/dwarfs.reducer';
import { DwarfsComponent } from './dwarfs.component';

const routes: Routes = [
  { path: '', component: DwarfsComponent },
  { path: ':lordId', component: DwarfsComponent },
];

@NgModule({
  declarations: [DwarfsComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    StoreModule.forFeature(DWARFS_FEATURE_KEY, dwarfsReducer),
    EffectsModule.forFeature([DwarfsEffects]),
    ProgressSpinnerModule,
    GuideSharedModule,
  ],
})
export class DwarfsModule {}
