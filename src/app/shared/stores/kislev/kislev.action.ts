import { createAction, props } from '@ngrx/store';
import { FactionGuide } from '../../models/guide.model';

export const loadKislev = createAction('[KISLEV] Load Guide');
export const loadKislevSuccess = createAction(
  '[KISLEV] Load Guide Success',
  props<{ faction: FactionGuide }>()
);
export const loadKislevFailure = createAction(
  '[KISLEV] Load Guide Failure',
  props<{ error: string }>()
);
