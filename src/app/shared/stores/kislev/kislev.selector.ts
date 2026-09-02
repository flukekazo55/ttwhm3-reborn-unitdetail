import { createFeatureSelector, createSelector } from '@ngrx/store';
import { FactionGuideState, FactionGuideViewModel } from '../../models/guide.model';
import { KISLEV_FEATURE_KEY } from './kislev.reducer';

export const selectKislevState = createFeatureSelector<FactionGuideState>(KISLEV_FEATURE_KEY);

export const selectKislevVm = createSelector(
  selectKislevState,
  (state): FactionGuideViewModel => ({
    faction: state.faction,
    loading: state.loading,
    error: state.error,
  })
);
