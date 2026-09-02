import { createFeatureSelector, createSelector } from '@ngrx/store';
import { FactionGuideState, FactionGuideViewModel } from '../../models/guide.model';
import { KHORNE_FEATURE_KEY } from './khorne.reducer';

export const selectKhorneState = createFeatureSelector<FactionGuideState>(KHORNE_FEATURE_KEY);

export const selectKhorneVm = createSelector(
  selectKhorneState,
  (state): FactionGuideViewModel => ({
    faction: state.faction,
    loading: state.loading,
    error: state.error,
  })
);
