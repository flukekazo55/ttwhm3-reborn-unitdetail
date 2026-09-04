import { createAction, props } from '@ngrx/store';
import { FactionGuide } from '../../models/guide.model';

export const loadCathay = createAction('[CATHAY] Load Guide');
export const loadCathaySuccess = createAction(
  '[CATHAY] Load Guide Success',
  props<{ faction: FactionGuide }>()
);
export const loadCathayFailure = createAction(
  '[CATHAY] Load Guide Failure',
  props<{ error: string }>()
);
