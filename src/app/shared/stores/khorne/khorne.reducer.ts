import { createReducer, on } from '@ngrx/store';
import { FactionGuideState } from '../../models/guide.model';
import { loadKhorne, loadKhorneFailure, loadKhorneSuccess } from './khorne.action';

export const KHORNE_FEATURE_KEY = 'khorneGuide';

export const initialState: FactionGuideState = {
  faction: null,
  loading: false,
  error: null,
};

export const khorneReducer = createReducer(
  initialState,
  on(loadKhorne, (state) => ({ ...state, loading: true, error: null })),
  on(loadKhorneSuccess, (state, { faction }) => ({ ...state, faction, loading: false })),
  on(loadKhorneFailure, (state, { error }) => ({ ...state, loading: false, error }))
);
