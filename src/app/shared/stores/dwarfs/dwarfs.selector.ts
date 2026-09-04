import { createFeatureSelector, createSelector } from '@ngrx/store';
import { FactionGuideState, FactionGuideViewModel } from '../../models/guide.model';
import { DWARFS_FEATURE_KEY } from './dwarfs.reducer';

export const selectDwarfsState = createFeatureSelector<FactionGuideState>(DWARFS_FEATURE_KEY);

export const selectDwarfsVm = createSelector(
  selectDwarfsState,
  (state): FactionGuideViewModel => ({
    faction: state.faction,
    loading: state.loading,
    error: state.error,
  })
);
