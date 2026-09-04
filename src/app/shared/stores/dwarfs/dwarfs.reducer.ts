import { createReducer, on } from '@ngrx/store';
import { FactionGuideState } from '../../models/guide.model';
import { loadDwarfs, loadDwarfsFailure, loadDwarfsSuccess } from './dwarfs.action';

export const DWARFS_FEATURE_KEY = 'dwarfsGuide';

export const initialState: FactionGuideState = {
  faction: null,
  loading: false,
  error: null,
};

export const dwarfsReducer = createReducer(
  initialState,
  on(loadDwarfs, (state) => ({ ...state, loading: true, error: null })),
  on(loadDwarfsSuccess, (state, { faction }) => ({ ...state, faction, loading: false })),
  on(loadDwarfsFailure, (state, { error }) => ({ ...state, loading: false, error }))
);
