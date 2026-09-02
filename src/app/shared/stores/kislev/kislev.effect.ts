import { HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, of, switchMap } from 'rxjs';
import { KislevService } from '../../../services/kislev/kislev.service';
import { loadKislev, loadKislevFailure, loadKislevSuccess } from './kislev.action';

@Injectable()
export class KislevEffects {
  private actions$ = inject(Actions);
  private service = inject(KislevService);

  loadGuide$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadKislev),
      switchMap(() =>
        this.service.getFaction().pipe(
          map((faction) => loadKislevSuccess({ faction })),
          catchError((error: unknown) => {
            const message = error instanceof HttpErrorResponse
              ? `โหลดข้อมูลไม่สำเร็จ (${error.status})`
              : error instanceof Error
                ? error.message
                : 'โหลดข้อมูลไม่สำเร็จ';
            return of(loadKislevFailure({ error: message }));
          })
        )
      )
    )
  );
}
