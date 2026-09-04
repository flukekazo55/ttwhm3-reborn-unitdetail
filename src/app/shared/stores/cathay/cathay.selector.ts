import { createFeatureSelector, createSelector } from '@ngrx/store';
import { FactionGuideState, FactionGuideViewModel } from '../../models/guide.model';
import { CATHAY_FEATURE_KEY } from './cathay.reducer';

export const selectCathayState = createFeatureSelector<FactionGuideState>(CATHAY_FEATURE_KEY);

export const selectCathayVm = createSelector(
  selectCathayState,
  (state): FactionGuideViewModel => ({
    faction: state.faction,
    loading: state.loading,
    error: state.error,
  })
);
