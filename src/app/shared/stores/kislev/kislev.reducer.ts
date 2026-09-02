import { createReducer, on } from '@ngrx/store';
import { FactionGuideState } from '../../models/guide.model';
import { loadKislev, loadKislevFailure, loadKislevSuccess } from './kislev.action';

export const KISLEV_FEATURE_KEY = 'kislevGuide';

export const initialState: FactionGuideState = {
  faction: null,
  loading: false,
  error: null,
};

export const kislevReducer = createReducer(
  initialState,
  on(loadKislev, (state) => ({ ...state, loading: true, error: null })),
  on(loadKislevSuccess, (state, { faction }) => ({ ...state, faction, loading: false })),
  on(loadKislevFailure, (state, { error }) => ({ ...state, loading: false, error }))
);
