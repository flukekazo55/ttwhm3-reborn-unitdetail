import { createAction, props } from '@ngrx/store';
import { FactionGuide } from '../../models/guide.model';

export const loadKhorne = createAction('[KHORNE] Load Guide');
export const loadKhorneSuccess = createAction(
  '[KHORNE] Load Guide Success',
  props<{ faction: FactionGuide }>()
);
export const loadKhorneFailure = createAction(
  '[KHORNE] Load Guide Failure',
  props<{ error: string }>()
);
