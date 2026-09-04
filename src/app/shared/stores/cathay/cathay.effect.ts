import { HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, of, switchMap } from 'rxjs';
import { CathayService } from '../../../services/cathay/cathay.service';
import { loadCathay, loadCathayFailure, loadCathaySuccess } from './cathay.action';

@Injectable()
export class CathayEffects {
  private actions$ = inject(Actions);
  private service = inject(CathayService);

  loadGuide$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadCathay),
      switchMap(() =>
        this.service.getFaction().pipe(
          map((faction) => loadCathaySuccess({ faction })),
          catchError((error: unknown) => {
            const message = error instanceof HttpErrorResponse
              ? `โหลดข้อมูลไม่สำเร็จ (${error.status})`
              : error instanceof Error
                ? error.message
                : 'โหลดข้อมูลไม่สำเร็จ';
            return of(loadCathayFailure({ error: message }));
          })
        )
      )
    )
  );
}
