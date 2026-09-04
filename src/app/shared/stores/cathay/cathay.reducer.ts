import { createReducer, on } from '@ngrx/store';
import { FactionGuideState } from '../../models/guide.model';
import { loadCathay, loadCathayFailure, loadCathaySuccess } from './cathay.action';

export const CATHAY_FEATURE_KEY = 'cathayGuide';

export const initialState: FactionGuideState = {
  faction: null,
  loading: false,
  error: null,
};

export const cathayReducer = createReducer(
  initialState,
  on(loadCathay, (state) => ({ ...state, loading: true, error: null })),
  on(loadCathaySuccess, (state, { faction }) => ({ ...state, faction, loading: false })),
  on(loadCathayFailure, (state, { error }) => ({ ...state, loading: false, error }))
);
