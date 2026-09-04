import { createAction, props } from '@ngrx/store';
import { FactionGuide } from '../../models/guide.model';

export const loadDwarfs = createAction('[DWARFS] Load Guide');
export const loadDwarfsSuccess = createAction(
  '[DWARFS] Load Guide Success',
  props<{ faction: FactionGuide }>()
);
export const loadDwarfsFailure = createAction(
  '[DWARFS] Load Guide Failure',
  props<{ error: string }>()
);
